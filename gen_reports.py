#!/usr/bin/env python
# -*- coding: utf-8 -*-
from glob import glob
from os import listdir
from os.path import abspath, dirname, join
from subprocess import call

root_dir = dirname(abspath(__file__))
data_dir = join(root_dir, 'data')
cr_bin = '/Users/maurice_schoenmakers/Documents/workspace/todomvc/examples/node_modules/.bin/cr'
example_dir = '/Users/maurice_schoenmakers/Documents/workspace/todomvc/examples'

print data_dir
print cr_bin
print example_dir

projects = listdir(example_dir)

for project in projects:
    project_dir = join(example_dir, project)
    json_file = join(data_dir, project + '.json') 
    print json_file
    if project != 'angular-dart':
        call('%s -f json -o %s %s' % (cr_bin, json_file, project_dir), shell=True)
