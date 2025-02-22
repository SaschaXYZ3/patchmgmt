# Ansible Playbook for Checkmk Installation

This Ansible project automates the installation of Checkmk, including downloading, verification, installation, and creating a monitoring instance.

## Directory Structure

```
ansible-checkmk/                # Main directory of the Ansible project
│-- inventory                   # Inventory file for target hosts
│-- playbook.yml                 # Main playbook (includes roles)
│-- roles/                       # Folder for all roles
│   │-- 01_checkmk_download/     # Role: Download Checkmk
│   │   │-- tasks/
│   │   │   ├── main.yml
│   │-- 02_checkmk_verify/       # Role: Verify Checkmk SHA256
│   │   │-- tasks/
│   │   │   ├── main.yml
│   │-- 03_checkmk_install/      # Role: Install Checkmk
│   │   │-- tasks/
│   │   │   ├── main.yml
│   │-- 04_checkmk_create_instance/ # Role: Create Checkmk instance
│   │   │-- tasks/
│   │   │   ├── main.yml
```

## Prerequisites

- A Linux server running Debian/Ubuntu (tested with **Ubuntu 24.04 Noble**)
- Ansible installed on the control node (`sudo apt install ansible`)
- SSH access to target hosts with sufficient permissions

## Usage

### 1️ **Adjust Inventory**

Modify the `inventory` file and add your target hosts:

```
[checkmk_servers]
server1.example.com
server2.example.com
```

### 2️ **Run the Playbook**

Execute the playbook to install Checkmk:

```sh
ansible-playbook -i inventory playbook.yml
```

### 3️ **Start Checkmk Instance**

After successful installation, start the instance with:

```sh
sudo omd start monitoring
```

## Role Descriptions

### **01_checkmk_download**

- Downloads the Checkmk package:  
  `wget https://download.checkmk.com/checkmk/2.3.0p27/check-mk-raw-2.3.0p27_0.noble_amd64.deb`

### **02_checkmk_verify**

- Verifies the integrity of the package using the SHA256 checksum:  
  `e318c0c1d1c7b91fdc639d89a1a05d0820614a854dbc19aef7c6719e35a9905a`

### **03_checkmk_install**

- Installs the package using `apt`
- Verifies installation with `omd version`

### **04_checkmk_create_instance**

- Creates a new Checkmk monitoring instance using `omd create monitoring`
- Displays a message on how to start the instance

## Extensions

- **Use variables:** Store SHA256, download URL, and instance name in `group_vars` or `host_vars`
- **Centralized configuration:** Provide adjustable settings using an additional `config.yml`
- **Backup & Restore:** Automatically back up the Checkmk instance before updates
