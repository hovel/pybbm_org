#!/bin/bash

echo $3 > pass
ansible-playbook -i ~/deploy-inventory/ansible/inventory/production_mini/hosts build/deploy.yml --vault-password-file pass -e "@build/vars/production.yml"