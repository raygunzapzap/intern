import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import altair as alt
import seaborn as sns
from vega_datasets import data
from matplotlib.colors import LinearSegmentedColormap

chart = pd.read_csv('t2.csv', sep=',')
#Set the stagnant data at NaN

first_idx = chart[chart["temperature"] > 30].index[0]# first index
last_idx = chart[chart["temperature"] > 90].index[-1]# last index
#Shortens the data by only using the chunk in between stagnant values
newData = chart.iloc[first_idx:last_idx+1]

#Calculate the differences between values
newData['dtemp'] = newData['temperature'].diff()

#Calculate the moving range
newData['matemp'] = newData['temperature'].rolling(window=20).mean()

#Calculate the change  in the moving range values
newData['dmatemp'] = newData['matemp'].diff()



#Create column to track cycles
cooling = False
start = 0
end = 0
newData['cycles'] = np.nan
cycle_count = 1
#Append to the cycles column if value is starting or ending a cycle

for i in range(len(newData)):
    if not np.isnan(newData.iloc[i]['dmatemp']):
        if not cooling:
            if newData.iloc[i]['dmatemp'] < 0:
                cooling = True
        else:
            if i + 1 == len(newData):
                end = i
                newData['cycles'][start:end+1] = cycle_count
            else:
                if (newData.iloc[i]['dmatemp'] > 0) and (newData.iloc[i + 1]['dmatemp'] > 0):
                    if (i + 2) < (len(newData) - 1) and (newData.iloc[i + 2]['dmatemp'] > 0):
                        end = i - 1
                        # cycles.append([start, end])
                        newData['cycles'][start:end] = cycle_count
                        cycle_count += 1
                        start = end
                        end = start
                        cooling = False
               
newCycle = newData.groupby('cycles').head(1)

            
newCycle['diff'] = newCycle['time'].diff()


# diagnostic plots of results
fig, axs = plt.subplots(2, 1, figsize=(40,14))

x = newData['time']
y = newData['temperature']
z = newCycle['time']

# for i in newCycle['time']:
#     plt.axvline(i,0,1,color='red')

# plt.xlim(1907.025373, 2386.541297)
# plt.plot(x, y,)
# plt.show()

#plt.xlim(2386.541297, 2993.022848)

# axs[0].plot(x, y)
# axs[0].set_xlim(1907.025373, 2386.541297)

# axs[1].plot(x, y)
# axs[1].set_xlim(44237.022209, 44657.537605)


input_dropdown = alt.binding_select(options=['Cycle 1','Cycle 2','Cycle 3',
                                              'Cycle 4','Cycle 5','Cycle 6',
                                              'Cycle 7','Cycle 8','Cycle 9',
                                              'Cycle 10','Cycle 11','Cycle 12',
                                              'Cycle 13','Cycle 14','Cycle 15',
                                              'Cycle 16','Cycle 17','Cycle 18',
                                              'Cycle 19','Cycle 20','Cycle 21',
                                              'Cycle 22','Cycle 23','Cycle 24',
                                              'Cycle 25','Cycle 26','Cycle 27'])



brush = alt.selection_interval(zoom=True)  # selection of type "interval"


#ax = sns.countplot(x="temperature",data=newData)
# fig, ax = plt.subplots()
# newData['temperature'].value_counts().plot(ax = ax, kind = 'bar')

#newData.sort_values(by=['temperature'])

# make a custom colormap with transparency
# ncolors = 256
# color_array = plt.get_cmap('YlOrRd')(range(ncolors))
# color_array[:, -1] = np.linspace(0, 1, ncolors)
# cmap = LinearSegmentedColormap.from_list(name='YlOrRd_alpha', colors=color_array)
# plt.hist2d(y, y,  bins=[50, 5], cmap=cmap, edgecolor='white')
# plt.show()


# chart = alt.Chart(newData).mark_line().encode(
#    x='time',
#    y='temperature',
# ).interactive().add_selection(
#     brush)

# chart = alt.Chart(newData).mark_line().encode(
#    x='time',
#    y='temperature',
#    color=alt.condition(brush, 'Cycle:N', alt.value('gray'))
# ).add_selection(
#     brush)

alt.Chart(newData).mark_boxplot().encode(
    x='cycles:O',
    y='temperature:Q'
).save('box.html')

alt.data_transformers.disable_max_rows()


#chart1 = alt.Chart(newCycle).mark_rule().encode(x='time', opacity=alt.value(0.8), color=alt.value('orange'))#.interactive()

#alt.layer(chart1, chart).save('chart.html')




        


