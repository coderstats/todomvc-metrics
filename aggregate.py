#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
    'Sum Physical SLOC',
    'Sum Logical SLOC',
    'Sum files',
    'Sum functions',
    'Mean Maintainability index',
    'Mean parameter count',
    #'Mean cyclomatic complexity',
    #'Mean Halstead difficulty',
    #'Mean Halstead volume',
    #'Mean Halstead effort',
    #'Mean functions per file',
)

stats = defaultdict(dict)
stats.fromkeys(metrics)


for report in reports:
    project = os.path.splitext(os.path.basename(report))[0]
    with open(report, 'r') as f:
        project_files = json.load(f)
        stats['Sum files'][project] = len(project_files)
        for project_file in project_files:
            stats['Sum Logical SLOC'][project] = stats['Sum Logical SLOC'].get(project, 0) + project_file['aggregate']['complexity']['sloc']['logical']
            stats['Sum Physical SLOC'][project] = stats['Sum Physical SLOC'].get(project, 0) + project_file['aggregate']['complexity']['sloc']['physical']
            stats['Mean Maintainability index'][project] = stats['Mean Maintainability index'].get(project, 0) + project_file['maintainability']
            stats['Mean parameter count'][project] = stats['Mean parameter count'].get(project, 0) + project_file['params']
            stats['Sum functions'][project] = stats['Sum functions'].get(project, 0) + len(project_file['functions'])


#print [(k, v) for k, v in sorted(stats['Sum files'].items(), key=lambda x: x[1], reverse=True)]
for metric in stats:
    values = list(stats[metric].values())
    if metric in ['Mean Maintainability index', 'Mean parameter count']:
        try:
            counts = list(stats['Sum files'].values())
        except:
            continue
        values = [v / counts[i] for i, v in enumerate(values)]
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