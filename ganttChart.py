import numpy as np
import datetime
import matplotlib.pylab as plt
import matplotlib.dates as mdates
import pandas as pd

# Style
plt.style.use("bmh")
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

base = datetime.datetime(2021, 1, 21)
dates = np.array([base + datetime.timedelta(days=(i))
                  for i in range(60)])

N = len(dates)
np.random.seed(19680801)
y = np.cumsum(np.random.randn(N))

fig, ax = plt.subplots(constrained_layout=True)


#format the ticks
ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=range(1,32), interval=10))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%B %d'))
ax.xaxis.set_minor_locator(mdates.DayLocator(bymonthday=range(1,32)))

ax.set_yticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5])
ax.set_yticklabels(['task1', 'task2', 'task3', 'task4', 'task5', 'task6', 'task7', 'task8', 'task9', 'task10'])
ax.set_xlim(mdates.date2num(dates[0]), mdates.date2num(dates[-1]))
ax.set_ylim(0,10)

#broken barh
#ax.broken_barh([(mdates.date2num(dates[0]), mdates.date2num(dates[10]))], (2,1), facecolors = ('tab:red'))
ax.broken_barh([(mdates.date2num(dates[2]), 10)], (0.125, .75), facecolors='tab:cyan')
ax.broken_barh([(mdates.date2num(dates[4]), 10)], (1.125, .75), facecolors='tab:cyan')
ax.broken_barh([(mdates.date2num(dates[8]), 10)], (2.125, .75), facecolors='tab:cyan')
ax.broken_barh([(mdates.date2num(dates[12]), 10)], (3.125, .75), facecolors='tab:cyan')
ax.broken_barh([(mdates.date2num(dates[20]), 10)], (4.125, .75), facecolors='tab:cyan')
ax.broken_barh([(mdates.date2num(dates[23]), 10)], (5.125, .75), facecolors='tab:cyan')
ax.broken_barh([(mdates.date2num(dates[26]), 10)], (6.125, .75), facecolors='tab:cyan')
ax.broken_barh([(mdates.date2num(dates[29]), 10)], (7.125, .75), facecolors='tab:cyan')
ax.broken_barh([(mdates.date2num(dates[38]), 10)], (8.125, .75), facecolors='tab:cyan')
ax.broken_barh([(mdates.date2num(dates[40]), 10)], (9.125, .75), facecolors='tab:cyan')


ax.set_title('L102 IDP Gantt Chart')

plt.xticks(rotation=30)

plt.savefig("L102ganttChart.png", dpi=600)
plt.show()
