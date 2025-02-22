#!/bin/bash

# Load Checkmk site environment
source /omd/sites/monitoring/.profile

# Define monitored hosts (Hostname, IP, Description)
HOSTS=(
  "server1 192.168.1.101 Ansible Server"
  "server2 192.168.1.102 Checkmk Server"
  "server3 192.168.1.103 Zammad Server"
  "server4 192.168.1.104 Jenkins"
  "server5 192.168.1.105 SIEM"
  "server6 192.168.1.106 DNS"
  "server7 192.168.1.107 DHCP"
)

# Loop through and add hosts to Checkmk
for host in "${HOSTS[@]}"; do
  set -- $host
  HOSTNAME=$1
  IP=$2
  DESCRIPTION=$3

  echo "Adding host: $HOSTNAME ($IP) - $DESCRIPTION"

  # Add the host to Checkmk
  cmk --add-host "$HOSTNAME" --ip "$IP" --alias "$DESCRIPTION"
done

# Apply changes and reload configuration
cmk -R

echo "Successfully added all hosts to Checkmk!"
