# -*- coding: utf-8 -*-
from fabric.api import local


def clone():
    local('git clone https://github.com/tastejs/todomvc.git')


# remove various files and directories not to include in calculations
def clean():
    #local('find todomvc/ -name "*.cache.js" -exec rm -rf {} \;')
    # omit gwt as it is written in Java
    local('rm -rf todomvc/architecture-examples/gwt/')

    # omit dart as it is written in dart
    local('rm -rf todomvc/architecture-examples/dart/')

    # remove specific libs users don't need to write themeselves
    local('rm -rf todomvc/architecture-examples/dojo/js/lib/')
    local('rm -rf todomvc/architecture-examples/knockback/js/lib/')
    local('rm -rf todomvc/architecture-examples/emberjs/js/libs/')

    # bower_components dir and minified js files before running cr
    local('find todomvc/ -type d -name bower_components -exec rm -rf {} \;')
    local('find todomvc/ -type f -name "*.min.js" -exec rm -rf {} \;')
    local('find todomvc/ -type f -name "*-compressed.js" -exec rm -rf {} \;')
    local('find todomvc/ -type f -name "*compiled.js" -exec rm -rf {} \;')

    # ignore dirs called test
    local('find todomvc/ -type d -name test -exec rm -rf {} \;')