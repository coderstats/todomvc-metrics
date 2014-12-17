##  !/usr/bin/env python
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
    'Sum Physical SLOC': ('aggregate', 'sloc', 'physical'),
    'Sum Logical SLOC': ('aggregate', 'sloc', 'logical'),
    'Mean Cyclomatic Complexity': ('aggregate', 'cyclomatic'),
    'Mean Maintainability Index': ('maintainability',),
    'Mean Parameter Count': ('params',),
    'Sum Halstead Difficulty': (
        'aggregate',  'halstead', 'difficulty'),
    'Sum Halstead Volume': ('aggregate', 'halstead', 'volume'),
    'Sum Halstead Effort': ('aggregate', 'halstead', 'effort'),
    'Sum Halstead Bugs': ('aggregate', 'halstead', 'bugs'),
    'Sum Halstead Time': ('aggregate', 'halstead', 'time'),
}

metrics = list(metrics_map.keys())

stats = defaultdict(dict)
stats.fromkeys(metrics)


def val_from_path(path, di):
    return reduce(lambda d, key: d[key], path, di)


for report in reports:
    project = os.path.splitext(os.path.basename(report))[0]
    with open(report, 'r') as f:
        project_files = json.load(f)['reports']
        print len(project_files)
        stats['Sum Files'][project] = len(project_files)
        for project_file in project_files:
            stats['Sum Functions'][project] = stats['Sum Functions'].get(
                project, 0) + len(project_file['functions'])

            for metric, path in list(metrics_map.items()):
                stats[metric][project] = stats[metric].get(
                    project, 0) + val_from_path(path, project_file)


for metric in stats:
    items = list(stats[metric].items())
    projects = []
    values = []

    # convert to lists so projects and values are aligned correctly
    for project, value in items:
        projects.append(project)
        values.append(value)

    if metric.startswith('Mean'):
        values = [
            value / stats['Sum Files'][projects[index]]
                for index, value in enumerate(values)
        ]

    stats[metric] = pd.Series(values, index=projects)


df = pd.DataFrame(stats)

# create a plot for each metric
for metric in stats:
    df = df.sort(metric, ascending=True)
    fig = plt.figure(figsize=(18, 18))

    axes = plt.Axes(fig, [.2, .1, .7, .8])  # [left, bottom, width, height]
    fig.add_axes(axes)

    df[metric].plot(kind='barh', title=metric, alpha=0.7)
    plt.savefig('images/' + metric.replace(' ', '-'))


# create csv
df.to_csv('data/todomvc-metrics.csv')

# create radviz
from pandas.tools.plotting import radviz

df_rad = df[
    ['Sum Logical SLOC',
    'Mean Cyclomatic Complexity',
    'Sum Halstead Time',
    'Mean Maintainability Index']]
df_rad['Name'] = df_rad.index.tolist()

fig = plt.figure(figsize=(18, 18))
ax = radviz(df_rad, 'Name')
legend = ax.legend(fontsize='xx-small', fancybox=True, ncol=3 )
plt.setp(legend.get_title(),fontsize='xx-small')
plt.savefig('images/radviz')
