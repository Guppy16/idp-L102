import numpy as np
import datetime
from matplotlib.lines import Line2D
import matplotlib.pylab as plt
import matplotlib.dates as mdates
import pandas as pd

# Style
plt.style.use("bmh")
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

base = datetime.datetime(2021, 1, 21)
dates = np.array([base + datetime.timedelta(days=(i))
                  for i in range(34)])


fig, ax = plt.subplots(constrained_layout=True)


#format the ticks
#ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=range(1,32), interval=7))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=1, interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%B %d'))
ax.xaxis.set_minor_locator(mdates.DayLocator(bymonthday=range(1,32)))

ax.set_yticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5])
ax.set_yticklabels(['Planning/onboarding', 'Presentation/report', 'CAD', 'Electronics', 'Software', 'Simulation/testing', 'Documentation', ])
ax.set_xlim(mdates.date2num(dates[0]), mdates.date2num(dates[-1]))
ax.set_ylim(0,7)

#broken barh
#ax.broken_barh([(mdates.date2num(dates[0]), mdates.date2num(dates[10]))], (2,1), facecolors = ('tab:red'))
#barcolor1='lightgray'
barcolor1='darkgray'
ax.broken_barh([(mdates.date2num(dates[0]), 2)], (0.125, .75), facecolors=barcolor1)
ax.broken_barh([(mdates.date2num(dates[2]), 10)], (2.125, .75), facecolors=barcolor1)
ax.broken_barh([(mdates.date2num(dates[2]), 10)], (3.125, .75), facecolors=barcolor1)
ax.broken_barh([(mdates.date2num(dates[2]), 10)], (4.125, .75), facecolors=barcolor1)
ax.broken_barh([(mdates.date2num(dates[10]), 17)], (5.125, .75), facecolors=barcolor1)
ax.broken_barh([(mdates.date2num(dates[17]), 15)], (6.125, .75), facecolors=barcolor1)
ax.broken_barh([(mdates.date2num(dates[3]), 4)], (1.125, .75), facecolors=barcolor1)
ax.broken_barh([(mdates.date2num(dates[24]), 2)], (1.125, .75), facecolors=barcolor1)
ax.broken_barh([(mdates.date2num(dates[29]), 3)], (1.125, .75), facecolors=barcolor1)

#deadline dates

plt.axvline(x=mdates.date2num(datetime.datetime(2021, 1, 26)), color='springgreen', linestyle='dashed', ymin=.025, ymax=.75)
plt.axvline(x=mdates.date2num(datetime.datetime(2021, 1, 28)), color='blue', linestyle='dashed', ymin=.025, ymax=.75)
plt.axvline(x=mdates.date2num(datetime.datetime(2021, 2, 2)), color='gold', linestyle='dashed', ymin=.025)
plt.axvline(x=mdates.date2num(datetime.datetime(2021, 2, 9)), color='gold', linestyle='dashed', ymin=.025)
plt.axvline(x=mdates.date2num(datetime.datetime(2021, 2, 11)), color='red', linestyle='dashed', ymin=.025)
plt.axvline(x=mdates.date2num(datetime.datetime(2021, 2, 16)), color='springgreen', linestyle='dashed', ymin=.025)
plt.axvline(x=mdates.date2num(datetime.datetime(2021, 2, 17)), color='red', linestyle='dashed', ymin=.025)
plt.axvline(x=mdates.date2num(datetime.datetime(2021, 2, 22)), color='blue', linestyle='dashed', ymin=.025)

ax.set_title('L102 IDP Gantt Chart')

#legend
custom_lines = [Line2D([0], [0], color = 'springgreen'), Line2D([0], [0], color = 'gold'), Line2D([0], [0], color = 'red'), Line2D([0], [0], color = 'blue')]

ax.legend(custom_lines,['Presentation', 'Progress Meeting', 'Competition', 'Report'], loc='upper left')

ax.grid(False)





plt.xticks(rotation=30)

plt.savefig("L102ganttChart.png", dpi=600)
plt.show()
