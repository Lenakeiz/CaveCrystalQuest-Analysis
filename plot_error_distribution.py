import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt

# from plot_trial_route generate production error csv file
folder_path = os.path.join(os.path.dirname(__file__),'output/error_stats') # Replace with the path to your folder
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

def arrange_array(arr):
    sorted_arr = np.sort(arr)
    arranged_arr = np.array([sorted_arr[0], 360 - sorted_arr[0], sorted_arr[1], 360 - sorted_arr[1]])
    return arranged_arr

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


# Is production the only source of angular error?
fig, axs = plt.subplots(1, 4, figsize=(16, 5))
arranged_homing_angles = arrange_array(combined_df['homing_angle'].unique())
for n,homing_angle in enumerate(arranged_homing_angles):
    subset = combined_df[combined_df['homing_angle'] == homing_angle]
    subset['angular_difference'] = subset['production_angle'] - homing_angle
    ax = axs[n]
    sns.color_palette("Set2")
    sns.histplot(data=subset, x='angular_difference', hue='encoding_angle', palette='Set2',kde=True, alpha=0.6, element='step',ax=axs[n])
    ax.axvline(x=0,linestyle=":")
    ax.set(xlabel='Angular Production Error',title=f'Homing Angle {homing_angle}°')   
plt.suptitle(f'Combined Histogram of Angular Error for Same Homing Angle and Different Encoding Angles',fontsize=16)   
plt.show()

# Is encoding the only source of angular error?
fig, axs = plt.subplots(1, 4, figsize=(16, 5))
arranged_encoding_angles = arrange_array(combined_df['encoding_angle'].unique())
for n,encoding_angle in enumerate(arranged_encoding_angles):
    subset = combined_df[combined_df['encoding_angle'] == encoding_angle]
    subset['angular_difference'] = subset['production_angle'] - subset['homing_angle']
    ax = axs[n]
    sns.color_palette("Set2")
    sns.histplot(data=subset, x='angular_difference', hue='homing_angle', palette='tab10',kde=True, alpha=0.6, element='step',ax=axs[n])
    ax.axvline(x=0,linestyle=":")
    ax.set(xlabel='Angular Production Error',title=f'Encoding Angle {encoding_angle}°')   
plt.suptitle(f'Combined Histogram of Angular Error for Same Encoding Angle and Different Homing Angles',fontsize=16)  
plt.show()


# # assign group based on homing angle and encoding angle
# homing_to_encoding = combined_df.groupby('homing_angle')['encoding_angle'].unique().to_dict()
# homing_to_encoding = {k: sorted(v) for k, v in homing_to_encoding.items() if len(v) == 2}
# def assign_Egroup(row):
#     encoding_angles = homing_to_encoding.get(row['homing_angle'])
#     if encoding_angles:
#         return 'EGroup1' if row['encoding_angle'] == encoding_angles[0] else 'EGroup2'
#     return 'Other'

# encoding_to_homing = combined_df.groupby('encoding_angle')['homing_angle'].unique().to_dict()
# encoding_to_homing = {k: sorted(v) for k, v in encoding_to_homing.items() if len(v) == 2}
# def assign_Hgroup(row):
#     homing_angles = encoding_to_homing.get(row['encoding_angle'])
#     if homing_angles:
#         return 'HGroup1' if row['encoding_angle'] == homing_angles[0] else 'HGroup2'
#     return 'Other'


# # homing angles centered at 180 degrees
# fig, axs = plt.subplots(1, 4, figsize=(16, 5))
# for n,encoding_angle in enumerate(combined_df['encoding_angle'].unique()):
#     subset = combined_df[combined_df['encoding_angle'] == encoding_angle]
#     if encoding_angle == 60 or encoding_angle == 300: 
        
#         ## homing angle centered to the smaller respectively
#         # subset.loc[subset['homing_angle'] == 240, 'production_angle'] /= 2  
        
#         # homing angle centered to 180 for all   
#         subset['production_angle'] = subset.apply(lambda row: row['production_angle'] * 0.75 if row['homing_angle'] == 240 else row['production_angle'] * 1.5, axis=1)
#     else:
#         # subset.loc[subset['homing_angle'] == 315, 'production_angle'] /= 7  
#         subset['production_angle'] = subset.apply(lambda row: row['production_angle'] * 4/7 if row['homing_angle'] == 315 else row['production_angle'] * 4, axis=1)       
#     ax = axs[n]
#     ax.axvline(x=180,linestyle=":",color="cyan")
#     sns.histplot(data=subset, x='production_angle', hue='homing_angle', palette='tab10',kde=True, alpha=0.6, element='step',ax=axs[n])
#     ax.set(xlabel='Production Angle',title=f'Encoding Angle {encoding_angle}°')  

# plt.suptitle(f'Combined Histogram of Same Encoding Angle and Different Homing Angles',fontsize=14)   
# plt.show()