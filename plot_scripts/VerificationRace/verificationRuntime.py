import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from os import listdir
from os.path import isfile, join

# VERIFICATIONRUNTIME DATA ONLY

DATASET = "./data/VerificationRace/bound30bw32"
SAMPLE_FRACTION = 1

filePaths = [f for f in listdir(DATASET) if isfile(join(DATASET, f))]

frames = []

for f in filePaths:
    frames.append(pd.read_csv(join(DATASET, f)))

df = pd.concat(frames, ignore_index=True)

df = df.sample(frac=SAMPLE_FRACTION)

# Scatter Catagorical Graph here

p = sns.stripplot(data=df, y="clock_time", x="type", hue="type", palette='icefire_r')


# SIMPLE BAR GRAPH HERE

# grouped_sum = df.groupby('type')['clock_time'].sum()
# gdf = grouped_sum.reset_index()    
# p = sns.barplot(data=gdf, x="type", y="clock_time", palette='icefire_r')


p.set_title(str(SAMPLE_FRACTION*100) + "% of Verification data from " + DATASET.split("/")[-1]+ " dataset"  )
p.set_xlabel( "Type") 
p.set_ylabel( "Seconds to complete each verification")
plt.show()