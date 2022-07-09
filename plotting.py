import pandas as pd
import matplotlib.patches as patches # for the legend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D # for the legend

df = pd.read_csv("C:/Users/azeem/Desktop/output.csv")

BLUE = "#3D85F7"
BLUE_LIGHT = "#5490FF"
PINK = "#C32E5A"
PINK_LIGHT = "#D34068"
GREY40 = "#666666"
GREY25 = "#404040"
GREY20 = "#333333"
BACKGROUND = "#F5F4EF"

plt.subplots(figsize=(12,7))

epochs = df["iter"].values

data = df["reward"].values
#ma2c = df["ff"].values

plt.plot(epochs, data, color='r')
#plt.plot(epochs, ma2c, color='r')


plt.margins(0.01)
plt.title("Average Reward Collected", size = 32, pad = 20)

plt.xlabel("Training iterations", labelpad = 15, size = 24)
plt.ylabel("Average Reward Collected", labelpad = 15, size = 24)
fig = plt.gcf()
fig.set_size_inches(21, 11.25)
#plt.savefig("avg_q.png", dpi = 1200)