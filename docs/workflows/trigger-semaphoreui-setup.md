# ⚙️ GitHub Action: Trigger Semaphore “Setup Semaphore” Task

## 📖 Purpose

This workflow ensures that the **Setup Semaphore** task inside the **Home Lab** project in Semaphore UI is automatically executed whenever relevant inventory changes are committed. Instead of running the `setup_semaphoreui.yml` playbook locally, this workflow delegates execution to Semaphore, keeping configuration application centralized, consistent, and environment‑controlled.

Whenever files under `inventory/semaphore/group_vars/semaphore/` are modified, the workflow runs the reusable `scripts/execute_semaphoreui_setup.py` script, which authenticates with Semaphore UI, locates the correct project and task template, and triggers a new execution.

---

## 🛠 Workflow File  
Located at: `.github/workflows/trigger-semaphoreui-setup.yml`

```yaml
name: Trigger Semaphore "Setup Semaphore" Task

on:
  push:
    paths:
      - "inventory/semaphore/group_vars/semaphore/**"

jobs:
  trigger-semaphore-task:
    runs-on: ubuntu-latest

    steps:
      # Checkout the repo
      - name: Checkout repository
        uses: actions/checkout@v4

      # Set up Python
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      # Install dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests

      # Execute the Semaphore trigger script
      - name: Trigger Semaphore task
        env:
          SEMAPHORE_URL: "https://semaphore.refol.us/api"
          SEMAPHORE_TOKEN: ${{ secrets.SEMAPHORE_API_TOKEN }}
          PROJECT_NAME: "Home Lab"
          TEMPLATE_NAME: "Setup Semaphore"
        run: |
          python scripts/execute_semaphoreui_setup.py
```

---

## 🔑 Key Points

- **Trigger:** Runs automatically whenever any file under  
  `inventory/semaphore/group_vars/semaphore/`  
  is added, modified, or removed.  
- **Checkout:** Uses `actions/checkout@v4` to pull the repository contents.  
- **Python Setup:** Uses Python 3.12 to run the API‑driven trigger script.  
- **Dependencies:** Installs only the `requests` library (lightweight and fast).  
- **Script Execution:**  
  - Calls `scripts/execute_semaphoreui_setup.py`, which:  
    - Authenticates with Semaphore UI  
    - Locates the **Home Lab** project  
    - Locates the **Setup Semaphore** task template  
    - Executes the template  
    - Prints the execution ID and monitoring URL  
- **Secrets:** Requires a repository secret named `SEMAPHORE_API_TOKEN`.  
- **Design Intent:** Keeps GitHub Actions lightweight while delegating configuration application to Semaphore, ensuring consistent execution environments and centralized automation.
