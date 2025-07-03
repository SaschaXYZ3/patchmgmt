# Patching with Ansible

This repository contains a playbook that can be used to patch both Red Hat-based and Debian-based systems.

## Configuration

In the `ansible.cfg` file, you must set the remote user:

```ini
remote_user = <your-remote-username>
```

In `group_vars/all/vault.yml`, you can store the encrypted password of the remote user.

## How to Encrypt the Password

To encrypt the password using Ansible Vault, use the following command:

```sh
ansible-vault encrypt_string '<Enter your password here>' --name <remote_user_variable_name>
New Vault password:
Confirm New Vault password:
Encryption successful
```

Store the password used to decrypt the vault in a file named `.vault`.

## Inventory

The `inventory` file defines which hosts the playbook should run against. You can specify hosts directly or organize them into groups.

all together

```ini
[all]
debian-host1.mydomain.com
debian-host2.mydomain.com
redhat-host1.mydomain.com
```

or by groups

```ini
[debian]
debian-host1.mydomain.com
debian-host2.mydomain.com

[redhat]
redhat-host1.mydomain.com
```

## Running the Playbook

You can now run the playbook without having to enter the Vault password manually:

```sh
ansible-playbook -i inventory patch.yml --vault-password-file .vault
```

### Optional: Limit to a Specific Host

You can limit the playbook run to a specific host or group using the `--limit` option:

limit to host

```sh
ansible-playbook -i inventory patch.yml --vault-password-file .vault --limit myhost.mydomain.com
```

limit to group

```sh
ansible-playbook -i inventory patch.yml --vault-password-file .vault --limit debian
```
