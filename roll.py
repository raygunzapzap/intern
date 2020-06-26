import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

data = pd.read_csv('t1.csv', sep=',')
# print(data.values)
# print(len(data.values))
# print(len(data.values[0]))

time = []
temp = []
# collect time and temp values in separate arrays
for i in range(len(data.values)):
# for i in range(600,1800):
  time.append(data.values[i][0])
  temp.append(data.values[i][1])

# calculate the change in temperature for one value to the next
dtemp = []
for i in range(len(time)):
  if i == 0:
    dtemp.append(float("NaN"))
  else:
    dtemp.append(temp[i] - temp[i-1])

# calculate a moving range average for the temperature values
matemp = []
# the moving average window size 
# this can be adjusted (14 seems close)
# this is the number of values to use for calculating the moving average
maspan = 14
for i in range(len(time)):
  if i < maspan:
    # we don't have enough values for the current moving average window size
    matemp.append(float("NaN"))
  else:
    ma = np.mean(temp[i-maspan:i])
    # print(temp[i-maspan:i])
    matemp.append(ma)

# calculate the change in moving range values from one to the next
dmatemp = []
for i in range(len(time)):
  if i < maspan:
    # we don't have enough values for the current moving average window size
    dmatemp.append(float("NaN"))
  else:
    dmatemp.append(matemp[i] - matemp[i-1])

cycles = []
cooling = False
start = 0
end = 0
# loop through the array containing changes in the moving range temp array
for i in range(len(time)):
  # ignore NaN values
  if not math.isnan(dmatemp[i]):
    # if we are in the heating phase, check for point where we switch to cooling values
    if not cooling:
      if dmatemp[i] < 0:
        cooling = True
    else:
      if i + 1 == len(time): # last value; end current cycle
        end = i
        cycles.append([start, end])
      else:
        # record a cycle if the current i value (and the two after it) are positive
        if (dmatemp[i] > 0) and (dmatemp[i + 1] > 0):
          if (i + 2) < (len(time) - 1) and (dmatemp[i + 2] > 0):
            end = i - 1
            cycles.append([start, end])
            start = end
            end = start
            cooling = False

# for i in range(len(cycles)):
#   print(cycles[i])

# diagnostic plots of results
fig, axs = plt.subplots(4, 1, figsize=(20,14))

# plot vertical line at time of detected cycles (plotting where the cycle ends)
for cycle in cycles:
  axs[0].axvline(x = time[cycle[1]], color='black')
axs[0].plot(time, temp)
axs[0].set_ylabel('temperature')
axs[0].grid(True)

axs[1].plot(time, dtemp)
axs[1].set_ylabel('temperature change')
axs[1].grid(True)

axs[2].plot(time, matemp)
axs[2].set_ylabel('moving average temperature')
axs[2].grid(True)

# plot vertical line at time of detected cycles (plotting where the cycle ends)
for cycle in cycles:
  axs[3].axvline(x = time[cycle[1]], color='black')
axs[3].plot(time, dmatemp)
axs[3].set_ylabel('moving average temperature change')
axs[3].grid(True)

# axs[3].axvline(x = 2500)

fig.tight_layout()
plt.show()