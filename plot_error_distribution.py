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

# f = sns.FacetGrid(combined_df, col='encoding_angle', col_wrap=4) 
# f.map(sns.histplot, 'angular_error',binwidth=0.05,kde=True)
# f.set(xlim=(0,2),xlabel='Angular Error')
# plt.show()

# g = sns.FacetGrid(combined_df, col='homing_angle', col_wrap=4)
# g.map(sns.histplot, 'angular_error',binwidth=0.05,kde=True)
# g.set(xlim=(0,2),xlabel='Angular Error')
# plt.show()

# h = sns.FacetGrid(combined_df, col='encoding_distance', col_wrap=4) 
# h.map(sns.histplot, 'linear_error',binwidth=0.05,kde=True)
# h.set(xlim=(0,2),xlabel='Linear Error')
# plt.show()


homing_to_encoding = combined_df.groupby('homing_angle')['encoding_angle'].unique().to_dict()
homing_to_encoding = {k: sorted(v) for k, v in homing_to_encoding.items() if len(v) == 2}

# Function to assign group based on homing angle and encoding angle
def assign_Egroup(row):
    encoding_angles = homing_to_encoding.get(row['homing_angle'])
    if encoding_angles:
        return 'EGroup1' if row['encoding_angle'] == encoding_angles[0] else 'EGroup2'
    return 'Other'

# # Add a new column for the group
# combined_df['encoding_group'] = combined_df.apply(assign_Egroup, axis=1)
# g = sns.FacetGrid(combined_df, row='encoding_group', col='homing_angle', margin_titles=True, height=3, aspect=1.5)
# g.map_dataframe(sns.histplot, 'production_angle',kde=True, alpha=0.6)
# g.set_axis_labels('Production Angle', 'Count')
# g.fig.subplots_adjust(top=0.9)
# g.fig.suptitle('Individual Histograms of Production Angles for Different Encoding Angles', fontsize=12)

fig, axs = plt.subplots(1, 4, figsize=(16, 5))
for n,homing_angle in enumerate(combined_df['homing_angle'].unique()):
    subset = combined_df[combined_df['homing_angle'] == homing_angle]
    subset['production_angle'] = subset['production_angle'] - homing_angle
    ax = axs[n]
    sns.color_palette("Set2")
    sns.histplot(data=subset, x='production_angle', hue='encoding_angle', palette='Set2',kde=True, alpha=0.6, element='step',ax=axs[n])
    ax.axvline(x=0,linestyle=":")
    ax.set(xlabel='Production Angle',title=f'Homing Angle {homing_angle}°')   
plt.suptitle(f'Combined Histogram of Angular Error for Same Homing Angle and Different Encoding Angles',fontsize=16)   
plt.show()

encoding_to_homing = combined_df.groupby('encoding_angle')['homing_angle'].unique().to_dict()
encoding_to_homing = {k: sorted(v) for k, v in encoding_to_homing.items() if len(v) == 2}

# Function to assign group based on homing angle and encoding angle
def assign_Hgroup(row):
    homing_angles = encoding_to_homing.get(row['encoding_angle'])
    if homing_angles:
        return 'EGroup1' if row['encoding_angle'] == homing_angles[0] else 'HGroup2'
    return 'Other'

fig, axs = plt.subplots(1, 4, figsize=(16, 5))
for n,encoding_angle in enumerate(combined_df['encoding_angle'].unique()):
    subset = combined_df[combined_df['encoding_angle'] == encoding_angle]
    if encoding_angle == 60 or encoding_angle == 300: 
        
        # homing angle centered to the smaller respectively
        # subset.loc[subset['homing_angle'] == 240, 'production_angle'] /= 2  
        
        # homing angle centered to 180 for all   
        subset['production_angle'] = subset.apply(lambda row: row['production_angle'] * 0.75 if row['homing_angle'] == 240 else row['production_angle'] * 1.5, axis=1)
    else:
        # subset.loc[subset['homing_angle'] == 315, 'production_angle'] /= 7  
        subset['production_angle'] = subset.apply(lambda row: row['production_angle'] * 4/7 if row['homing_angle'] == 315 else row['production_angle'] * 4, axis=1)       
    ax = axs[n]
    ax.axvline(x=180,linestyle=":",color="cyan")
    sns.histplot(data=subset, x='production_angle', hue='homing_angle', palette='tab10',kde=True, alpha=0.6, element='step',ax=axs[n])
    ax.set(xlabel='Production Angle',title=f'Encoding Angle {encoding_angle}°')  

plt.suptitle(f'Combined Histogram of Same Encoding Angle and Different Homing Angles',fontsize=14)   
plt.show()