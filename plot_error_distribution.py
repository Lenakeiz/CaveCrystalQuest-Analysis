import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

# from plot_trial_route generate production error csv file
folder_path = 'output/error_stats'  # Replace with the path to your folder
all_files = os.listdir(folder_path)

# List to hold data from all files
all_data = []

# Read each file and append its data to the list
for file in all_files:
    if file.endswith('.csv'):
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        all_data.append(df)

# Combine all data into a single DataFrame
combined_df = pd.concat(all_data, ignore_index=True)

f = sns.FacetGrid(combined_df, col='encoding_angle', col_wrap=4) 
f.map(sns.histplot, 'angular_error',binwidth=0.05,kde=True)
f.set(xlim=(0,2),xlabel='Angular Error')
plt.show()

g = sns.FacetGrid(combined_df, col='homing_angle', col_wrap=4)
g.map(sns.histplot, 'angular_error',binwidth=0.05,kde=True)
g.set(xlim=(0,2),xlabel='Angular Error')
plt.show()

h = sns.FacetGrid(combined_df, col='encoding_distance', col_wrap=4) 
h.map(sns.histplot, 'linear_error',binwidth=0.05,kde=True)
h.set(xlim=(0,2),xlabel='Linear Error')
plt.show()


