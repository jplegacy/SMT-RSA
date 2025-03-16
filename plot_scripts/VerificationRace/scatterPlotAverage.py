import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from os import listdir
from os.path import isfile, join


# VERIFICATIONRUNTIME DATA ONLY

DATASET = "./data/VerificationRace/bound30bw32"
SAMPLE_FRACTION = 0.1

filePaths = [f for f in listdir(DATASET) if isfile(join(DATASET, f))]

frames = []

for f in filePaths:
    frames.append(pd.read_csv(join(DATASET, f)))

df = pd.concat(frames, ignore_index=True)

# A way to establish distance between the four parameters
def euclidean_distance(row):
    return (row['P']**2 + row['Q']**2 + row['E']**2 + row['D']**2)**(1/2)
    
df['spread_metric'] = df.apply(euclidean_distance, axis=1)

df = df.sample(frac=SAMPLE_FRACTION)


p = sns.scatterplot(data=df, y="clock_time", x="spread_metric", hue="type", palette='icefire_r')

p.set_title(str(SAMPLE_FRACTION*100) + "% of " + "input spread metric data from " + DATASET.split("/")[-1]+ " dataset"  )
p.set_ylabel( "Time of Verification") 
p.set_xlabel( "Spread Metric (Euclidean Distance)")
plt.show()