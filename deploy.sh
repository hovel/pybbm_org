#!/bin/bash

echo $3 > pass
ansible-playbook -i ~/deploy-inventory/ansible/inventory/production_mini/hosts site_content/build/deploy.yml --vault-password-file pass -e "@site_content/build/vars/production.yml"