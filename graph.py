from pandas import read_csv
from matplotlib import pyplot
import csv
import numpy as np
series = read_csv('t1.csv', header=0, index_col=0)
temp = np.array(series['temperature'])
p = temp.max()
v = temp.min()
print p
print v
series.plot()
pyplot.style.use('classic')
pyplot.title('Data from t1')
pyplot.xlabel('Time')
pyplot.ylabel('Temperature')



pyplot.show()
