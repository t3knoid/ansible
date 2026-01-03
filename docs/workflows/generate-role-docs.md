---
title: "️ GitHub Action: Generate Ansible Role Docs"
---

# ⚙️ GitHub Action: Generate Ansible Role Docs

## 📖 Purpose
This workflow ensures that documentation for all Ansible roles is **automatically generated and kept up to date**.  
Whenever code is pushed or a pull request is opened, the workflow runs the [Generate Role Documentation Script](docs/roles/scripts/generate_role_docs.md), which regenerates each role’s `README.md`, and updates the central `roles/README.md` index. If changes are detected, they are committed back to the repository.

---

## 🛠 Workflow File
Located at: `.github/workflows/generate-role-docs.yml`

{% raw %}
```yaml
name: Generate Ansible Role Docs

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  generate-role-docs:
    # Only run the job logic when the branch is main
    if: github.ref == 'refs/heads/main'
    
    runs-on: ubuntu-latest

    steps:
      # Checkout the repo
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # needed for committing back

      # Set up Python
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      # Install dependencies (if any)
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # Run the documentation generator
      - name: Generate role docs
        run: |
          python ./scripts/generate_role_docs.py

      - name: Commit and push changes
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git pull origin main
          git add roles/README.md docs/roles/README.md docs/roles/*.md

          if ! git diff --cached --quiet; then
            git commit -m "chore(docs): auto-generate role documentation"
            git push origin main
          else
            echo "No documentation changes to commit."
          fi
```
{% endraw %}

---

## 📝 Summary

* **Trigger:** Runs on every push to `main` and on pull requests.  
* **Checkout:** Uses `actions/checkout@v4` with `fetch-depth: 0` so commits can be pushed back.  
* **Python Setup:** Uses Python 3.11 (adjustable).  
* **Dependencies:** Installs from `requirements.txt` (currently only PyYAML).  
* **Script Execution:** Runs `scripts/generate_role_docs.py` to regenerate role documentation.
* **Generated Documentation:** The following markdown files are created by the Python script:
  * `roles/README.md`
  * `docs/roles/README.md`
  * `docs/roles/<role folder name>.md`
* **Commit Logic:**  
  * Stages only role READMEs and the central index.  
  * Commits only if changes exist (`git diff --cached --quiet` prevents empty commits).  
  * Pushes back to the branch that triggered the workflow.  
* **Permissions:** Requires repository **Actions → Workflow permissions** set to **Read and write** so the built‑in `GITHUB_TOKEN` can push commits.
