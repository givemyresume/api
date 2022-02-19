#!/bin/sh

# Set the github token using `export GITHUB_TOKEN="ghp_NUpU9xxtwrrq9Tz2nLx2Rc9Rjh3axxxxxxxx"`
cd givemyresume.github.io
echo "entered givemyresume.github.io"
git add .
echo "added all files"
git commit -m "add resume using script"
echo "committed the added files"
git push https://subhayu99:$GITHUB_TOKEN@github.com/givemyresume/givemyresume.github.io.git
echo "pushed to repo"
