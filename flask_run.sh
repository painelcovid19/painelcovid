#!/bin/bash

app=$1
debug=$2

export FLASK_APP=${app}
export FLASK_DEBUG=${debug}

flask run
