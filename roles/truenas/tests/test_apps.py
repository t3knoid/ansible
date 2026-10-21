import importlib.util
from pathlib import Path
import unittest
from unittest.mock import Mock, patch


SPEC = importlib.util.spec_from_file_location(
    "truenas_api", Path(__file__).resolve().parents[1] / "library" / "truenas_api.py"
)
API = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(API)


class AppJobTests(unittest.TestCase):
    def test_waits_for_success(self):
        transport = Mock()
        transport.call.side_effect = [7, [{"state": "RUNNING"}], [{"state": "SUCCESS", "result": True}]]
        with patch.object(API.time, "sleep"):
            self.assertTrue(API.app_job(transport, "app.create", [{}], 30, 1))
        self.assertEqual(transport.call.call_args_list[1].args, ("core.get_jobs", [["id", "=", 7]]))

    def test_failed_job_does_not_leak_error_payload(self):
        transport = Mock()
        transport.call.side_effect = [7, [{"state": "FAILED", "error": "secret-password"}]]
        with self.assertRaisesRegex(API.MiddlewareError, "ended in FAILED") as raised:
            API.app_job(transport, "app.update", ["example", {}], 30, 1)
        self.assertNotIn("secret-password", str(raised.exception))

    def test_timeout_leaves_job_for_operator_review(self):
        transport = Mock()
        transport.call.side_effect = [7, [{"state": "RUNNING"}]]
        with patch.object(API.time, "monotonic", side_effect=[0, 2]):
            with self.assertRaisesRegex(API.MiddlewareError, "may still be running"):
                API.app_job(transport, "app.create", [{}], 1, 1)

    def test_requires_numeric_job_id(self):
        transport = Mock()
        transport.call.return_value = {"id": "example"}
        with self.assertRaisesRegex(API.MiddlewareError, "job ID"):
            API.app_job(transport, "app.create", [{}], 30, 1)


class AppComparisonTests(unittest.TestCase):
    def test_catalog_defaults_are_not_drift(self):
        self.assertTrue(API.app_config_matches({"port": 8080}, {"port": 8080, "default": True}))

    def test_ordered_lists_are_compared_in_order(self):
        self.assertFalse(API.app_config_matches({"command": ["first", "second"]}, {"command": ["second", "first"]}))

    def test_scalar_types_are_not_coerced(self):
        self.assertFalse(API.app_config_matches({"enabled": True}, {"enabled": 1}))


class AppHealthTests(unittest.TestCase):
    def test_waits_for_desired_runtime(self):
        transport = Mock()
        transport.call.side_effect = [[{"state": "DEPLOYING"}], [{"state": "RUNNING"}]]
        with patch.object(API.time, "sleep"):
            self.assertEqual(API.app_wait_state(transport, "example", "RUNNING", 30, 1), "RUNNING")

    def test_absence_after_deletion(self):
        transport = Mock()
        transport.call.return_value = []
        self.assertEqual(API.app_wait_state(transport, "example", "ABSENT", 30, 1), "ABSENT")

    def test_health_timeout_is_not_success(self):
        transport = Mock()
        transport.call.return_value = [{"state": "CRASHED"}]
        with patch.object(API.time, "monotonic", side_effect=[0, 2]):
            with self.assertRaisesRegex(API.MiddlewareError, "did not reach RUNNING"):
                API.app_wait_state(transport, "example", "RUNNING", 1, 1)


class AppDeploymentTests(unittest.TestCase):
    def setUp(self):
        self.module = Mock()
        self.module.check_mode = False
        self.module.params = {
            "app": {"name": "example", "source": "custom", "compose": "services:\n  web:\n    image: nginx:1.28\n"},
            "app_apply": True,
            "app_job_timeout": 30,
            "app_health_timeout": 30,
            "app_poll_interval": 1,
        }
        self.compose = {"services": {"web": {"image": "nginx:1.28"}}}
        self.current = {"id": "example", "state": "RUNNING", "custom_app": True}
        self.transport = Mock()

    def test_custom_create_uses_structured_compose_and_waits(self):
        self.transport.call.side_effect = [[], [self.current]]
        with patch.object(API, "app_job") as job, patch.object(API, "app_wait_state", return_value="RUNNING"):
            result = API.run_app(self.module, self.transport)
        self.assertTrue(result["changed"])
        self.assertEqual(job.call_args.args[1], "app.create")
        self.assertEqual(job.call_args.args[2][0]["custom_compose_config"], self.compose)

    def test_missing_app_deletion_is_noop(self):
        self.module.params["app"]["state"] = "absent"
        self.transport.call.return_value = []
        self.assertFalse(API.run_app(self.module, self.transport)["changed"])

    def test_unknown_fields_are_refused(self):
        self.module.params["app"]["runtime_typo"] = "stopped"
        with self.assertRaisesRegex(API.MiddlewareError, "Unrecognized"):
            API.run_app(self.module, self.transport)
        self.transport.call.assert_not_called()

    def test_job_failure_stops_runtime_actions(self):
        self.transport.call.return_value = []
        with patch.object(API, "app_job", side_effect=API.MiddlewareError("job failed")):
            with self.assertRaisesRegex(API.MiddlewareError, "job failed"):
                API.run_app(self.module, self.transport)
        self.assertEqual(self.transport.call.call_count, 1)

    def test_custom_noop_is_idempotent(self):
        self.transport.call.side_effect = [[self.current], self.compose, [self.current]]
        with patch.object(API, "app_job") as job, patch.object(API, "app_wait_state", return_value="RUNNING"):
            self.assertFalse(API.run_app(self.module, self.transport)["changed"])
        job.assert_not_called()

    def test_custom_removed_keys_trigger_update(self):
        self.transport.call.side_effect = [[self.current], dict(self.compose, networks={}), [self.current]]
        with patch.object(API, "app_job") as job, patch.object(API, "app_wait_state", return_value="RUNNING"):
            self.assertEqual(API.run_app(self.module, self.transport)["actions"], ["update"])
        self.assertEqual(job.call_args.args[1], "app.update")

    def test_plan_never_mutates(self):
        self.module.params["app_apply"] = False
        self.transport.call.return_value = []
        with patch.object(API, "app_job") as job:
            self.assertEqual(API.run_app(self.module, self.transport)["actions"], ["create"])
        job.assert_not_called()

    def test_check_mode_never_mutates(self):
        self.module.check_mode = True
        self.transport.call.return_value = []
        with patch.object(API, "app_job") as job:
            self.assertTrue(API.run_app(self.module, self.transport)["planned"])
        job.assert_not_called()

    def test_delete_requires_approval(self):
        self.module.params["app"]["state"] = "absent"
        self.transport.call.return_value = [self.current]
        with patch.object(API, "app_job") as job:
            with self.assertRaisesRegex(API.MiddlewareError, "allow_delete"):
                API.run_app(self.module, self.transport)
        job.assert_not_called()

    def test_delete_preserves_ix_volumes_and_images(self):
        self.module.params["app"].update(state="absent", allow_delete=True)
        self.transport.call.return_value = [self.current]
        with patch.object(API, "app_job") as job, patch.object(API, "app_wait_state", return_value="ABSENT"):
            self.assertEqual(API.run_app(self.module, self.transport)["actions"], ["delete"])
        self.assertEqual(job.call_args.args[2], ["example", {"remove_images": False, "remove_ix_volumes": False}])

    def test_source_conversion_is_refused(self):
        self.transport.call.return_value = [dict(self.current, custom_app=False)]
        with self.assertRaisesRegex(API.MiddlewareError, "source differs"):
            API.run_app(self.module, self.transport)

    def test_invalid_compose_rejected_before_discovery(self):
        self.module.params["app"]["compose"] = "services: []"
        with self.assertRaisesRegex(API.MiddlewareError, "services mapping"):
            API.run_app(self.module, self.transport)
        self.transport.call.assert_not_called()

    def catalog_setup(self):
        self.module.params["app"] = {
            "name": "example", "source": "catalog",
            "catalog": {"app": "arbitrary-app", "train": "stable", "version": "2.0.0"},
            "values": {"settings": {"port": 8080}},
        }
        self.current = dict(self.current, custom_app=False, version="2.0.0", metadata={"name": "arbitrary-app", "train": "stable"})

    def test_catalog_defaults_do_not_trigger_update(self):
        self.catalog_setup()
        self.transport.call.side_effect = [[self.current], {"settings": {"port": 8080, "other": True}}, [self.current]]
        with patch.object(API, "app_job") as job, patch.object(API, "app_wait_state", return_value="RUNNING"):
            self.assertFalse(API.run_app(self.module, self.transport)["changed"])
        job.assert_not_called()

    def test_catalog_create_is_generic(self):
        self.catalog_setup()
        self.transport.call.side_effect = [[], [self.current]]
        with patch.object(API, "app_job") as job, patch.object(API, "app_wait_state", return_value="RUNNING"):
            self.assertTrue(API.run_app(self.module, self.transport)["changed"])
        self.assertEqual(job.call_args.args[2][0], {
            "app_name": "example", "custom_app": False,
            "catalog_app": "arbitrary-app", "train": "stable", "version": "2.0.0",
            "values": {"settings": {"port": 8080}},
        })

    def test_catalog_identity_change_is_refused(self):
        self.catalog_setup()
        self.current["metadata"]["train"] = "another-train"
        self.transport.call.return_value = [self.current]
        with self.assertRaisesRegex(API.MiddlewareError, "catalog app/train differs"):
            API.run_app(self.module, self.transport)

    def test_catalog_update_preserves_unmanaged_nested_values(self):
        self.catalog_setup()
        self.transport.call.side_effect = [[self.current], {"settings": {"port": 80, "other": True}}, [self.current]]
        with patch.object(API, "app_job") as job, patch.object(API, "app_wait_state", return_value="RUNNING"):
            self.assertEqual(API.run_app(self.module, self.transport)["actions"], ["update"])
        self.assertEqual(job.call_args.args[2][1], {"values": {"settings": {"port": 8080, "other": True}}})

    def test_catalog_upgrade_requires_approval(self):
        self.catalog_setup()
        self.current["version"] = "1.0.0"
        self.transport.call.side_effect = [[self.current], {}]
        with patch.object(API, "app_job") as job:
            with self.assertRaisesRegex(API.MiddlewareError, "allow_upgrade"):
                API.run_app(self.module, self.transport)
        job.assert_not_called()

    def test_catalog_upgrade_uses_explicit_version(self):
        self.catalog_setup()
        self.current["version"] = "1.0.0"
        self.module.params["app"]["allow_upgrade"] = True
        self.transport.call.side_effect = [[self.current], {}, {"upgrade_version": "2.0.0"}, [self.current]]
        with patch.object(API, "app_job") as job, patch.object(API, "app_wait_state", return_value="RUNNING"):
            self.assertEqual(API.run_app(self.module, self.transport)["actions"], ["upgrade"])
        self.assertEqual(job.call_args.args[1], "app.upgrade")
        self.assertEqual(job.call_args.args[2][1]["app_version"], "2.0.0")

    def test_running_state_can_be_stopped(self):
        self.module.params["app"]["runtime"] = "stopped"
        self.transport.call.side_effect = [[self.current], self.compose, [self.current]]
        with patch.object(API, "app_job") as job, patch.object(API, "app_wait_state", return_value="STOPPED"):
            self.assertEqual(API.run_app(self.module, self.transport)["actions"], ["stop"])
        self.assertEqual(job.call_args.args[1], "app.stop")

    def test_stopped_state_can_be_started(self):
        self.current["state"] = "STOPPED"
        self.transport.call.side_effect = [[self.current], self.compose, [self.current]]
        with patch.object(API, "app_job") as job, patch.object(API, "app_wait_state", return_value="RUNNING"):
            self.assertEqual(API.run_app(self.module, self.transport)["actions"], ["start"])
        self.assertEqual(job.call_args.args[1], "app.start")


if __name__ == "__main__":
    unittest.main()