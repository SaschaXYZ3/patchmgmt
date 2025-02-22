Infrastructure Monitoring and Patch Management with Checkmk, Ansible, and Zammad

# Project Overview

This project provides an automated solution for monitoring RedHat-based and Debian-based systems using Checkmk. It ensures patch compliance by integrating with various plugins and triggers automated patching workflows using Ansible and a Change Request (CRQ) system via Zammad.

## Architecture

### Monitoring with Checkmk

Systems are monitored using Checkmk, which gathers information about their patch state.

The following plugins are used for tracking patch status:

Checkmk Agent Plugin for Yum (RedHat-based systems)

Checkmk Integration for APT (Debian-based systems)

### Automated Change Request (CRQ) Handling

Checkmk triggers an Ansible playbook to create a Change Request (CRQ) in Zammad.

The CRQ follows an approval workflow before executing any changes.

### Automated Patching

Once approved, Ansible automatically applies the required patches to the target systems.

## Client Responsibilities

Customers can integrate their systems into this monitoring and patch management solution, but they are responsible for:

Ensuring their systems are connected to a proper repository for updates.

Providing a user account with sufficient privileges to install the Checkmk agent and apply patches.

## Security & User Management

User credentials are securely stored using Ansible Vault, ensuring encrypted storage of sensitive data.

## Getting Started

Deploy Checkmk to monitor target systems.

Install the appropriate agent plugin for the system type.

Configure Ansible to trigger CRQ creation in Zammad.

Approve changes via Zammad.

Apply patches using Ansible after approval.
