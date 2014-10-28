#!/bin/bash

echo $3 > pass
cp ~/deploy-inventory/ansible/playbooks/deploy_app.yml build/deploy.yml
ansible-playbook -i ~/deploy-inventory/ansible/inventory/production_mini/hosts build/deploy.yml --vault-password-file pass -e "@build/vars/production.yml"