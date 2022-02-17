#!/usr/bin/bash

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

# Set the github token using `export GITHUB_TOKEN="ghp_NUpU9xxtwrrq9Tz2nLx2Rc9Rjh3axxxxxxxx"`
git add *
git commit -m "add resume using script"
git push https://subhayu99:$GITHUB_TOKEN@github.com/subhayu99/resume_builder_api.git --all
