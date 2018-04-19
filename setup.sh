#!/usr/bin/env bash

function eval_in_virtual_environment {
    command -v python3 >/dev/null 2>&1 || { echo >&2 "\`python3\` is required to run solar_django, please install it with \`brew install python3\`.  Aborting."; exit 1; }
    command -v virtualenv >/dev/null 2>&1 || { echo >&2 "\`virtualenv\` is required to run solar_django, please install it with \`pip3 install virtualenv\`.  Aborting."; exit 1; }

    VIRTUALENV_NAME=env
    if [ ! -d ${VIRTUALENV_NAME} ]; then
      virtualenv ${VIRTUALENV_NAME} -p python3
    fi

    source ${VIRTUALENV_NAME}/bin/activate

    export ALLOWED_HOSTS="localhost"
    export DEBUG="True"
    export SECRET_KEY="dl&)(n-z!^4*du2#jkg%2wfup8h-n_5in%*l7qx@4i(l#0skk4"
    export PORT=8000

    pip install --upgrade pip
    pip install --upgrade wheel
    pip install -r requirements.txt

    echo "Running '$1' inside virtual environment…"
    $1
}
