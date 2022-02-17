#!/usr/bin/bash

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
TOKEN=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

cd $SCRIPTPATH
git add *
git branch -M main
git commit -m "add resume using script"
git push https://subhayu99:$TOKEN@github.com/subhayu99/saved_resumes.git
cd -