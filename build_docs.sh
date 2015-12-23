#!/usr/bin/env bash

cd ./docs
make html
cd ../
touch .nojekyll

git checkout gh-pages

cp -rf ./docs/_build/html/* ./

git add .nojekyll *.html searchindex.js objects.inv _static/ _sources/
git commit -m "updated docs html build."
git pull origin gh-pages
git push origin gh-pages

git checkout -f master

rm -rf .nojekyll ./*.html searchindex.js objects.inv _static/ _sources/
