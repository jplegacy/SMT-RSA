
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from os import listdir
from os.path import isfile, join


# EncryptionRace DATA ONLY

DATASET = "./data/EncryptionRace/e200000d500"

filePaths = [f for f in listdir(DATASET) if isfile(join(DATASET, f))]

frames = []

for f in filePaths:
    frames.append(pd.read_csv(join(DATASET, f)))

df = pd.concat(frames, ignore_index=True)

p = sns.ecdfplot(data=df,hue="type", log_scale=True, x="clock_time", stat="count",palette='icefire_r')

p.set_title("Time to find decryption key: " + DATASET)
p.set_xlabel( "Runtime of each process log(s)") 
p.set_ylabel( "Number of Process")
plt.show()