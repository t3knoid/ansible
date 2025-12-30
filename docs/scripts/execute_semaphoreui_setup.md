# 🐍 Script: `execute_semaphoreui_setup.py`

## 📖 Purpose

This script provides a lightweight, API‑driven interface for triggering a Semaphore UI task template by name. It is used by GitHub Actions to execute the **Setup Semaphore** task inside the **Home Lab** project whenever inventory changes occur.  

Instead of running Ansible locally, this script delegates execution to Semaphore UI, ensuring consistent environments, centralized automation, and a clean separation between **desired state** (Git) and **state application** (Semaphore).

---

## 📁 Location  
`scripts/execute_semaphoreui_setup.py`

---

## 🧠 What the Script Does

The script performs the following steps:

1. **Reads required environment variables**  
   - Semaphore API URL  
   - API token  
   - Project name  
   - Template name  

2. **Authenticates with Semaphore UI** using a Bearer token.

3. **Fetches all projects** and locates the one matching `PROJECT_NAME`.

4. **Fetches all templates** within that project and locates the one matching `TEMPLATE_NAME`.

5. **Executes the template** using Semaphore’s REST API.

6. **Prints execution details**, including:  
   - Execution ID  
   - Direct monitoring URL  

This makes it easy for GitHub Actions logs to link directly to the running task.

---

## 🔧 Environment Variables

The script relies entirely on environment variables for configuration:

| Variable Name       | Description |
|---------------------|-------------|
| `SEMAPHORE_URL`     | Base API URL (e.g., `https://semaphore.refol.us/api`) |
| `SEMAPHORE_TOKEN`   | API token used for authentication |
| `PROJECT_NAME`      | Name of the Semaphore project (e.g., `Home Lab`) |
| `TEMPLATE_NAME`     | Name of the task template to execute (e.g., `Setup Semaphore`) |

These are injected by GitHub Actions, but the script can also be run locally by exporting the same variables.

---

## 🛠 Script Structure

The script is intentionally simple and modular:

- `get_env()`  
  Ensures required environment variables are present.

- `fetch_project_id()`  
  Retrieves the project list and finds the matching project.

- `fetch_template_id()`  
  Retrieves templates for the project and finds the matching template.

- `execute_template()`  
  Sends the API request to start a new task execution.

- `main()`  
  Orchestrates the full flow and prints results.

---

## ▶️ Example Usage (Local)

You can run the script manually for testing:

```bash
export SEMAPHORE_URL="https://semaphore.refol.us/api"
export SEMAPHORE_TOKEN="your-token-here"
export PROJECT_NAME="Home Lab"
export TEMPLATE_NAME="Setup Semaphore"

python scripts/execute_semaphoreui_setup.py
```

This will trigger the task and print the execution URL.

---

## 🔑 Key Points

- **No hard‑coded IDs** — the script resolves project and template IDs dynamically.  
- **API‑driven** — uses Semaphore’s REST API for all operations.  
- **Reusable** — can be called from GitHub Actions, CLI, or other automation.  
- **Minimal dependencies** — only requires the `requests` library.  
- **Contributor‑friendly** — clear error messages and explicit environment variables.

---

## 🧩 Related Documentation

- **Workflow:**  
  [`trigger-semaphoreui-setup.yml`](../workflows/trigger-semaphoreui-setup.md)

- **Semaphore UI:**  
  Project: *Home Lab*  
  Task Template: *Setup Semaphore*
