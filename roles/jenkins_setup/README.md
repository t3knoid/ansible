# 🛠️ Role: `jenkins_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Debian | Ubuntu](https://img.shields.io/badge/platforms-Debian%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs and configures Jenkins on Debian/Ubuntu systems.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Debian` (buster, bullseye)
- Supported on: `Ubuntu` (noble)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `jenkins_setup_version` | `2.492.1` | defaults file for jenkins_setup |
| `jenkins_setup_war` | `"https://get-jenkins.io/war-stable/{{ jenkins_setup_version }}/jenkins.war"` |  |
| `jenkins_setup_home` | `/data/jenkins` |  |
| `jenkins_setup_repo_key_url` | `https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key` |  |
| `jenkins_setup_repo_key_local` | `/etc/apt/trusted.gpg.d/jenkins.asc` |  |
| `jenkins_setup_javaopts` | `>-` |  |
| `jenkins_setup_port` | `8080` |  |
| `jenkins_setup_plugins` | `` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Create Jenkins home folder
- Copy config.yaml
- Remove existing Jenkins repo key
- Add Jenkins apt repository key
- Remove existing Jenkins repo list file
- Update apt repository
- Install Jenkins
- Stop Jenkins service
- Create init.groovy.d folder
- Copy create_admin_account.groovy
- Modify JENKINS_HOME environment variable
- Set Jenkins WorkingDirectory
- Set Java options
- Set Jenkins port to listen to
- Set Jenkins user
- Set Jenkins group
- Set Jenkins port to listen to
- Reload systemd to apply changes
- Start Jenkins service
- Download jenkins-cli.jar
- Install plugins
- Safe restart Jenkins

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: jenkins_setup
```