#!/bin/bash

echo $3 > pass
cp ~/deploy-inventory/ansible/playbooks/deploy_app.yml build/deploy.yml
ansible-playbook -i ~/deploy-inventory/ansible/inventory/production_mini/hosts build/deploy.yml --vault-password-file pass -e "@build/vars/master.yml" -e hovel_repo_name=$1 -e hovel_branch_name=$2
