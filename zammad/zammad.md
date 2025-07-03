# Zammad Installation Guide

This guide outlines the installation of **Zammad**, an open-source ticketing system, on Ubuntu 24.04.

## 1. Install Requirements
Before starting the installation, you need to install some dependencies:

```bash
sudo apt install curl apt-transport-https gnupg
```

---

## 2. Check Operating System Version
It's important to ensure your system is running the correct version:

```bash
cat /etc/*release
```

---

## 3. Install Elasticsearch as a Requirement
Elasticsearch is required for Zammad and must be correctly configured:

### Add Elasticsearch Repository
```bash
sudo apt install apt-transport-https wget curl gnupg

sudo curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | \
  sudo gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/elasticsearch.gpg > /dev/null

sudo echo "deb [signed-by=/etc/apt/trusted.gpg.d/elasticsearch.gpg] https://artifacts.elastic.co/packages/7.x/apt stable main" | \
  sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list > /dev/null
```

### Install and Start Elasticsearch
```bash
sudo apt update
sudo apt install elasticsearch

sudo systemctl start elasticsearch.service
sudo systemctl enable elasticsearch.service
systemctl status elasticsearch.service
```

---

## 4. Configure and Verify Elasticsearch
To verify Elasticsearch is running correctly, use the following command:

```bash
curl -X GET "localhost:9200"
```

**Example Output:**
```json
{
  "name" : "template",
  "cluster_name" : "elasticsearch",
  "version" : {
    "number" : "7.17.28"
  },
  "tagline" : "You Know, for Search"
}
```

### Install Ingest Plugin (only for Elasticsearch <= 7)
If you are using Elasticsearch version 7 or lower, you need the `ingest-attachment` plugin:

```bash
sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install ingest-attachment
sudo systemctl restart elasticsearch.service
```

### Increase Virtual Memory Map Limit
Elasticsearch requires a higher memory map limit. This can be temporarily increased as follows:

```bash
sudo sysctl -w vm.max_map_count=262144
```

---

## 5. Install Zammad
Add the Zammad repository and install the package:

```bash
curl -fsSL https://dl.packager.io/srv/zammad/zammad/key | \
   gpg --dearmor | sudo tee /etc/apt/keyrings/pkgr-zammad.gpg > /dev/null

sudo echo "deb [signed-by=/etc/apt/keyrings/pkgr-zammad.gpg] https://dl.packager.io/srv/deb/zammad/zammad/stable/ubuntu 24.04 main" | \
   sudo tee /etc/apt/sources.list.d/zammad.list > /dev/null
```

---

## 6. Adjust Nginx Configuration
Add your own IP address and or FQDN to the Nginx configuration:

```bash
sudo vi /etc/nginx/sites-available/zammad.conf
```

Then restart the Nginx service:

```bash
sudo systemctl restart nginx
```

---

## 7. Configure Zammad WebGUI

1. Open the URL in your browser: `http://<SERVER-IP>`
2. Log in with the following default credentials:
   - **Username:** `admin`
   - **Password:** `Start123$Start`

---

## 8. Recommended Additional Configuration
- Ideally, a mail server and a DNS server should be available.
- Zammad should be directly integrated into your monitoring tool such as **Checkmk**.

