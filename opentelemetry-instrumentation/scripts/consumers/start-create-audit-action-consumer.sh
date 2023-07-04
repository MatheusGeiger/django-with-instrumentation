#!/usr/bin/env bash

set -e

python manage.py pubsub ${CREATE_AUDIT_ACTION_DESTINATION} django_template.apps.example.pubsub.create_audit_action_consumer.consumer