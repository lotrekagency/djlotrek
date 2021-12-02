#!/bin/bash


if ! command -v semantic-release &> /dev/null
then
    echo "🙅 'semantic-release' seems not in PATH, maybe you are not in dev venv."
    echo "Just create your venv and run 'pip install -r requirements-dev.txt'"
    exit
fi

echo "Here what we are going to do:"

semantic-release publish "$@" --noop

while true; do
    read -p "Do you wish to continue?" yn
    case $yn in
        [Yy]* ) semantic-release publish "$@"; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

