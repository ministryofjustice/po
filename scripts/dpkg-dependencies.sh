#!/bin/bash

value() {
    echo "$1" | cut -f2 -d' '
}

startswith() {
    case $2 in $1*) true;; *) false;; esac;
}

filter_name_and_version() {
    IFS=$'\n'
    local metadata=( $1 )
    for line in "${metadata[@]}"; do

        if startswith Package "$line"; then
            local name=$(value "$line")

        elif startswith Version "$line"; then
            local version=$(value "$line")
            echo "$name|$version"
        fi
    done
    unset IFS
}

json_pkg() {
    local name="${1%|*}"
    local ver="${1#*|}"
    printf '{"package": {"name": "%s", "version": "%s", "source": "apt"}}' "$name" "$ver"
}

json_format() {
    for pkg in "$@"; do
        if [ "$pkg" != "$1" ]; then printf ", "; fi
        json_pkg "$pkg"
    done
}

installed_packages_metadata() {
    dpkg --status $(dpkg --get-selections | cut -f1)
}

json_format $(filter_name_and_version "$(installed_packages_metadata)")
