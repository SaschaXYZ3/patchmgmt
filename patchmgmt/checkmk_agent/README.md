# Install Checkmk Agent

After downloading this Git project, you need to replace the agents in the directory
`patchmgmt/checkmk_agent/packages` with your own Checkmk agents.

These agents are used to install Checkmk under `/opt` and provide the `yum` and `apt` plugins to monitor the update status of your systems.

## Adjust Configuration

### Change Remote User and SSH Key

If needed, update the remote user or add an SSH key in the following file:

```bash
vi /patchmgmt/patchmgmt/checkmk_agent/ansible.cfg
```

### Edit the Inventory

Open the inventory file and add your desired hosts:

```bash
vi /patchmgmt/patchmgmt/checkmk_agent/inventory
```

**Example content of the inventory file:**

```ini
[Hostgroup]
host1.domain.com
```

---

## Run the Playbook

If you're using an SSH key, you can omit the `-k` option and just use `-K`:

```bash
ansible-playbook -i inventory.yml playbook.yml -K
```

---

## Notes

- `-k` → Prompt for SSH password
- `-K` → Prompt for `sudo` password
