import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

size = 0.3
r = 3*size+0.3
# vals = np.array([[25,25,0], [50,50,50], [12,4,2]])
vals = np.random.random((4,5,5))

# vals[np.where(vals < 0.95)] = 0
vals[np.where(vals < 0.5)] = 0
# vals[:,0,:] = 0

cmap0 = plt.colormaps["gnuplot2"](np.arange(4)*50)
cmap1 = plt.colormaps["gnuplot2"](np.arange(20)*10)
cmap2 = plt.colormaps["gnuplot2"](np.arange(100)*2)
# outer_colors = cmap(np.arange(3)*100)
# inner_colors = cmap(np.arange(3)*50)
# print(outer_colors)

# 0
ax.pie(vals.sum(axis=(1,2)), radius=r-2*size, colors=cmap0,
       wedgeprops=dict(width=size, edgecolor='w'))

# 1
ax.pie(vals.sum(axis=(1)).flatten(), radius=r-size, colors=cmap1,
       wedgeprops=dict(width=size, edgecolor='w'))

# 2
ax.pie(vals.flatten(), radius=r, colors=cmap2,
       wedgeprops=dict(width=size, edgecolor='w'))

ax.set(aspect="equal", title='Pie plot with `ax.pie`')
plt.savefig('output/nested_pie_chart.png',transparent=True)