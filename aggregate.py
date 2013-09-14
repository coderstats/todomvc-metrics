#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from glob import glob
from os.path import abspath, dirname, join
import os

root_dir = dirname(abspath(__file__))
data_dir = join(root_dir, 'data')
reports = glob(data_dir + '/*.json')

stats = {}

for report in reports:
    project = os.path.splitext(os.path.basename(report))[0]
    with open(report, 'r') as f:
        project_files = json.load(f)
        for project_file in project_files:
            stats[project] = stats.get(project, 0) + project_file['aggregate']['complexity']['sloc']['logical']

print [(k, v) for k, v in sorted(stats.items(), key=lambda x: x[1], reverse=True)]