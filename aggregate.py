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

metrics_map = {
    'Sum Physical SLOC': ('aggregate', 'complexity', 'sloc', 'physical'),
    'Sum Logical SLOC': ('aggregate', 'complexity', 'sloc', 'logical'),
    'Mean cyclomatic complexity': ('aggregate', 'complexity', 'cyclomatic'),
    'Mean maintainability index': ('maintainability',),
    'Mean parameter count': ('params',),
    'Mean Halstead difficulty': (
        'aggregate', 'complexity', 'halstead', 'difficulty'),
    'Mean Halstead volume': ('aggregate', 'complexity', 'halstead', 'volume'),
    'Mean Halstead effort': ('aggregate', 'complexity', 'halstead', 'effort'),
    #'Mean functions per file',
}

metrics = list(metrics_map.keys())

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
            stats['Sum functions'][project] = stats['Sum functions'].get(
                project, 0) + len(project_file['functions'])

            for metric, path in list(metrics_map.items()):
                stats[metric][project] = stats[metric].get(
                    project, 0) + val_from_path(path, project_file)


file_counts = list(stats['Sum files'].values())
func_counts = list(stats['Sum functions'].values())
for metric in stats:
    values = list(stats[metric].values())
    if metric in ['Mean maintainability index', 'Mean parameter count']:
        values = [v / file_counts[i] for i, v in enumerate(values)]
    elif metric in [
        'Mean cyclomatic complexity',
        'Mean Halstead difficulty',
        'Mean Halstead volume',
        'Mean Halstead effort']:
        values = [v / func_counts[i] for i, v in enumerate(values)]
    stats[metric] = pd.Series(values, index=list(stats[metric].keys()))

df = pd.DataFrame(stats)

for metric in stats:
    df = df.sort(metric, ascending=True)
    fig = plt.figure()

    axes = plt.Axes(fig, [.2, .1, .7, .8])  # [left, bottom, width, height]
    fig.add_axes(axes)

    df[metric].plot(kind='barh', title=metric, alpha=0.7)
    plt.savefig('images/' + metric.replace(' ', '-'))