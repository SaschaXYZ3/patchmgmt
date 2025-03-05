# Ansible Playbook for Checkmk Installation

This Ansible project automates the installation of Checkmk, including downloading, verification, installation, and creating a monitoring instance.

## Directory Structure

```
ansible-checkmk/              
|-- ansible.cfg            
│-- inventory               
│-- playbook.yml           
│-- group_vars/       
│   │-- all/     
│   │   ├── site.yml
│   │   ├── vault.yml             
│-- roles/                        
│   │-- 10_install_requirements/  
│   │   │-- tasks/
│   │   │   ├── main.yml
│   │-- 11_install_collection_checkmk.general/       
│   │   │-- tasks/
│   │   │   ├── main.yml
│   │-- 12_install_checkmk/      
│   │   │-- tasks/
│   │   │   ├── main.yml
│   │-- 13_create_site/
│   │   │-- tasks/
│   │   │   ├── main.yml
|   |-- 14_set_webui_admin/
|   |   │-- tasks/
│   │   │   ├── main.yml
|   |-- 15_add_basic_clients/
|   |   │-- tasks/
│   │   │   ├── main.yml
```

## Prerequisites

- A Linux server running Debian/Ubuntu (tested with **Ubuntu 24.04 Noble**)
- Ansible installed on the control node (`sudo apt install ansible`)
- SSH access to target hosts with sufficient permissions

## Usage

### 1️ **Install Requirements**

```sh
sudo apt update && sudo apt upgrade -y
sudo apt install git ansible python3-pip -y
ansible-galaxy collection install checkmk.general
```
OR

```sh
ansible-playbook require.yml --ask-become-pass
```
### 2️ **Set variables for installation**

Set all neccessary variables for the installation in ./checkmk/group_vars/all/site.yml

```sh
checkmk_server_url: "http://192.168.1.245" # FQDN or IP of Checkmk Server, include http(s)://
checkmk_automation_user: "automation"
downloadlink: "https://download.checkmk.com/checkmk/2.3.0p27/check-mk-cloud-2.3.0p27_0.noble_amd64.deb" # actual downloadlink of the checkmk version you want to use
download_hash: "5c14d3689bde23bd4ef241744e54fb2674574d6b5ac1fb9fc40b87c8b6f09156" # actual hash value from the download you want to use
site_name: "monitoring" # the site name you monitoring instance should have
cmk_ip: "192.168.1.245" # the ip of your monitoring server, to add itself for monitoring
```
How to create a vault entry?
 
```sh
ansible-vault encrypt_string 'SuperSicheresPasswort123!' --name cmkadmin_password
New Vault password:
Confirm New Vault password:
Encryption successful
```
Save the encryption in vault file like __group_vars/all/vault.yml__

### 3 **Run the Playbook**

Execute the playbook in /patchmgmt/checkmk to install Checkmk:

```sh
ansible-playbook playbook.yml --ask-become-pass --ask-vault-pass
```

## Role Descriptions

### **10_install_requirements**

- 

### **11_install_collection_checkmk.general**

- 

### **12_install_checkmk**

- 

### **13_create_site**

- 

### **14_set_webui_admin**

- 

### **15_add_basic_clients**

- 
