#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import listdir
from os.path import abspath, dirname, join
from subprocess import call

root_dir = dirname(abspath(__file__))
data_dir = join(root_dir, 'data')
cr_bin = join(root_dir, 'node_modules/.bin/cr')
example_dir = root_dir + '/todomvc/examples'

for project in listdir(example_dir):
    project_dir = join(example_dir, project)
    json_file = join(data_dir, project + '.json')
    print('Generating report for project: %s' % project)
    call('%s -f json -o %s %s' % (cr_bin, json_file, project_dir), shell=True)
