"""
Trigger a Semaphore UI task template by name.

This script:
- Authenticates with Semaphore UI using an API token
- Finds a project by name
- Finds a task template by name
- Executes the template
- Prints the execution ID and monitoring URL

Environment variables required:
    SEMAPHORE_URL      Base API URL, e.g. https://semaphore.refol.us/api
    SEMAPHORE_TOKEN    API token for authentication
    PROJECT_NAME       Name of the Semaphore project (e.g., "Home Lab")
    TEMPLATE_NAME      Name of the task template (e.g., "Setup Semaphore")
"""

import os
import sys
import requests

def fail(message: str):
    """Print an error and exit."""
    print(f"❌ {message}")
    sys.exit(1)

def get_env(name: str) -> str:
    """Fetch a required environment variable."""
    value = os.environ.get(name)
    if not value:
        fail(f"Missing required environment variable: {name}")
    return value

def fetch_project_id(base_url: str, headers: dict, project_name: str) -> int:
    """Return the project ID for a given project name."""
    resp = requests.get(f"{base_url}/projects", headers=headers)
    if resp.status_code != 200:
        fail(f"Failed to fetch projects: {resp.text}")

    for project in resp.json():
        if project.get("name") == project_name:
            return project["id"]

    fail(f"Project '{project_name}' not found")

def fetch_template_id(base_url: str, headers: dict, project_id: int, template_name: str) -> int:
    """Return the template ID for a given template name."""
    resp = requests.get(f"{base_url}/project/{project_id}/templates", headers=headers)
    if resp.status_code != 200:
        fail(f"Failed to fetch templates: {resp.text}")

    for template in resp.json():
        if template.get("name") == template_name:
            return template["id"]

    fail(f"Template '{template_name}' not found in project ID {project_id}")

def execute_template(base_url: str, headers: dict, project_id: int, template_id: int) -> int:
    """Execute a template and return the execution ID."""
    resp = requests.post(
        f"{base_url}/project/{project_id}/tasks",
        headers=headers,
        json={"template_id": template_id}
    )

    if not 200 <= resp.status_code < 300:
        fail(f"Execution failed: {resp.text}")

    data = resp.json()
    execution_id = data.get("id")
    if not execution_id:
        fail(f"Execution response missing ID: {data}")

    return execution_id

def main():
    base_url = get_env("SEMAPHORE_URL")
    token = get_env("SEMAPHORE_TOKEN")
    project_name = get_env("PROJECT_NAME")
    template_name = get_env("TEMPLATE_NAME")

    headers = {"Authorization": f"Bearer {token}"}

    print(f"🔐 Authenticating with Semaphore UI at {base_url}")

    project_id = fetch_project_id(base_url, headers, project_name)
    print(f"📁 Found project '{project_name}' (ID: {project_id})")

    template_id = fetch_template_id(base_url, headers, project_id, template_name)
    print(f"📄 Found template '{template_name}' (ID: {template_id})")

    execution_id = execute_template(base_url, headers, project_id, template_id)
    execution_url = f"{base_url}/project/{project_id}/tasks/{execution_id}"

    print("🚀 Execution started!")
    print(f"   Execution ID: {execution_id}")
    print(f"   Monitor at: {execution_url}")

if __name__ == "__main__":
    main()
