#!/bin/bash

# Set the github token using `export GITHUB_TOKEN="ghp_NUpU9xxtwrrq9Tz2nLx2Rc9Rjh3axxxxxxxx"`
git add * saved_data/*
git commit -m "add resume using script"
git push https://subhayu99:$GITHUB_TOKEN@github.com/subhayu99/resume_builder_api.git
