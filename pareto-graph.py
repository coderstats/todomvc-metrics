# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

metric = 'Times Dominated'

fig = plt.figure()
axes = plt.Axes(fig, [.2, .1, .7, .8])  # [left, bottom, width, height]
fig.add_axes(axes)

df = pd.read_csv('data/pareto-ranking.csv', index_col=0)
df = df.sort(metric, ascending=False)
df[metric].plot(kind='barh', title=metric, alpha=0.7)
plt.savefig('images/%s' % metric.replace(' ', '-'))