#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import json
import os

import pandas as pd
import matplotlib.pyplot as plt

from collections import defaultdict
from glob import glob


root_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(root_dir, 'data')
reports = glob(data_dir + '/*.json')

metrics = (
    ('Sum Physical SLOC', ('aggregate', 'complexity', 'sloc', 'logical'),
    'Sum Logical SLOC',
    'Sum files',
    'Sum functions',
    'Mean cyclomatic complexity',
    'Mean maintainability index',
    'Mean parameter count',
    'Mean Halstead difficulty',
    'Mean Halstead volume',
    'Mean Halstead effort',
    #'Mean functions per file',
)

stats = defaultdict(dict)
stats.fromkeys(metrics)


def val_from_path(path, di):
    return reduce(lambda d, key: d[key], path, di)


for report in reports:
    project = os.path.splitext(os.path.basename(report))[0]
    with open(report, 'r') as f:
        project_files = json.load(f)
        stats['Sum files'][project] = len(project_files)
        for project_file in project_files:
            stats['Sum Logical SLOC'][project] = stats['Sum Logical SLOC'].get(project, 0) + project_file['aggregate']['complexity']['sloc']['logical']
            stats['Sum Physical SLOC'][project] = stats['Sum Physical SLOC'].get(project, 0) + project_file['aggregate']['complexity']['sloc']['physical']
            stats['Sum functions'][project] = stats['Sum functions'].get(project, 0) + len(project_file['functions'])
            stats['Mean maintainability index'][project] = stats['Mean maintainability index'].get(project, 0) + project_file['maintainability']
            stats['Mean cyclomatic complexity'][project] = stats['Mean cyclomatic complexity'].get(project, 0) + project_file['aggregate']['complexity']['cyclomatic']
            stats['Mean Halstead difficulty'][project] = stats['Mean Halstead difficulty'].get(project, 0) + project_file['aggregate']['complexity']['halstead']['difficulty']
            stats['Mean Halstead volume'][project] = stats['Mean Halstead volume'].get(project, 0) + project_file['aggregate']['complexity']['halstead']['volume']
            stats['Mean Halstead effort'][project] = stats['Mean Halstead effort'].get(project, 0) + project_file['aggregate']['complexity']['halstead']['effort']
            stats['Mean parameter count'][project] = stats['Mean parameter count'].get(project, 0) + project_file['params']


file_counts = list(stats['Sum files'].values())
func_counts = list(stats['Sum functions'].values())
for metric in stats:
    values = list(stats[metric].values())
    if metric in ['Mean maintainability index', 'Mean parameter count']:
        values = [v / file_counts[i] for i, v in enumerate(values)]
    elif metric in ['Mean cyclomatic complexity', 'Mean Halstead difficulty', 'Mean Halstead volume', 'Mean Halstead effort']:
        values = [v / func_counts[i] for i, v in enumerate(values)]
    stats[metric] = pd.Series(values, index=list(stats[metric].keys()))

df = pd.DataFrame(stats)

for metric in stats:
    df = df.sort(metric, ascending=True)
    fig = plt.figure()

    axes = plt.Axes(fig, [.2,.1,.7,.8]) # [left, bottom, width, height]
    fig.add_axes(axes)

    #plt.margins = 1000
    df[metric].plot(kind='barh', title=metric, alpha=0.7)
    plt.savefig('images/' + metric.replace(' ', '-'))