#!/usr/bin/env bash

source ./setup.sh

MANAGE_SUBCOMMAND=$1

function manage {
    python manage.py $MANAGE_SUBCOMMAND
}

eval_in_virtual_environment manage
