#!/bin/bash

dependencies() {
    script_path="$( cd "$(dirname "$0")" ; pwd -P )"
    dpkg_dependencies=$(/bin/bash "${script_path}/dpkg-dependencies.sh")
    printf "$dpkg_dependencies"
}

deployment() {
    # ENV
    #  - the name of the deployment environment, eg: "staging"
    #  - this is usually set in template-deploy
    # APP_BUILD_TAG
    #  - The name of the build, eg: "jenkins-BUILD-postcodeinfo-482"
    #  - this is usually set for use by ping.json
    # PROJECT
    #  - the name of the project, eg: "CLA Public"
    #  - this is usually set in template deploy
    printf '{"environment": "%s", "build": {"name": "%s", "product": {"name": "%s"}, "dependencies": [%s]}}' "$ENV" "$APP_BUILD_TAG" "$PROJECT" "$1"
}

post() {
    url="http://${PO_API_HOST}:8000/deployments/"
    curl -vvvv -u andy:uhxs527 -X "POST" -H "Content-Type: application/json" -d "${1}" "${url}"
}

post "$(deployment "$(dependencies)")"
