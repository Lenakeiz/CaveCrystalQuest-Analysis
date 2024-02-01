import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from config import excluded_dict

folder_path = os.path.join(os.path.dirname(__file__),'output/error_stats') # Replace with the path to your folder
all_files = os.listdir(folder_path)
all_data = []
for file in all_files:
    if file.endswith('.csv'):
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        all_data.append(df)
combined_df = pd.concat(all_data, ignore_index=True)
exclude_mask = combined_df.apply(lambda df: (df['subject_id'], df['trial_number']) in excluded_dict, axis=1)
combined_df = combined_df[~exclude_mask]
combined_df['start_positions'] = 'x = ' + combined_df['start_position_x'].astype(str) + '  y = ' + combined_df['start_position_z'].astype(str)
combined_df['location_error_x'] = combined_df['target_position_x'] - combined_df['start_position_x']
combined_df['location_error_z'] = combined_df['target_position_z'] - combined_df['start_position_z']
combined_df['is_reflex_angle'] = combined_df['encoding_angle'] > 180
arranged_encoding_distance = np.sort(combined_df['encoding_distance'].unique())
arranged_start_positions = np.sort(combined_df['start_positions'].unique())
arranged_encoding_angles = np.sort(combined_df['encoding_angle'].unique())
arranged_is_reflex = combined_df['is_reflex_angle'].unique()


# # all encoding distance in one histogram for production distance
# sns.histplot(data=combined_df, x='production_distance', hue='encoding_distance',binwidth=0.1,palette="flare",kde=True, alpha=0.3, element='step',edgecolor = 'none')
# plt.xlabel('Linear Production')
# for n, value in enumerate(arranged_encoding_distance):
#     plt.axvline(x=value, linestyle='--', color=sns.color_palette("flare")[round(1.8*n)])
# plt.show()


# # histograms for linear error
# fig, axs = plt.subplots(1, 4, figsize=(16, 5))
# for n,encoding_distance in enumerate(arranged_encoding_distance):
#     subset = combined_df[combined_df['encoding_distance'] == encoding_distance]
#     ax = axs[n]
#     sns.histplot(data=subset, x='linear_error', binwidth=0.2,color=sns.color_palette("flare")[n],kde=True, alpha=0.8, element='step',ax=axs[n])
#     ax.axvline(x=0,linestyle=":")
#     ax.set_xlim([-3,4])
#     ax.set(xlabel='Linear Production Error',title=f'Encoding Distance {encoding_distance}m')   
# plt.suptitle(f'Combined Histogram of Linear Error for Same Encoding Distance',fontsize=16)  
# plt.show()


# # all encoding distance in one histogram for location error
# sns.histplot(data=combined_df, x='location_error', hue='encoding_distance',binwidth=0.1,palette="dark:#5A9_r",kde=True, alpha=0.5, element='step',edgecolor = 'none')
# plt.xlabel('Distance from Starting Point(m)')
# plt.show()


# # one scatterplot of target positions grouped by start positions
# sns.scatterplot(data=combined_df, x='target_position_x',y='target_position_z', hue='start_positions',palette="Spectral_r")
# plt.show()

# # 4 scatterplots of target positions by start positions
# fig, axs = plt.subplots(1, 4, figsize=(16, 5))
# for n,start_positions in enumerate(arranged_start_positions):
#     subset = combined_df[combined_df['start_positions'] == start_positions]
#     start_position_x = subset['start_position_x'].unique()[0]
#     start_position_z = subset['start_position_z'].unique()[0]
#     print(start_position_x,start_position_z)
#     ax = axs[n]
#     sns.scatterplot(data=subset, x='target_position_x',y='target_position_z',color=sns.color_palette("dark:#5A9_r")[round(1.7*n)],alpha=0.8,ax=axs[n])
#     ax.scatter(start_position_x,start_position_z,c="#eb8a90",marker="^")
#     ax.set(xlabel='Target Location X',ylabel='Target Location Z')  
#     ax.set_xlim([-4,4])
#     ax.set_ylim([-4,4]) 
# plt.suptitle(f'Combined Scatterplot of Target Locations for Same Start Location',fontsize=16)  
# plt.show()


# #location error histograms by 4 encoding angles 
# fig, axs = plt.subplots(1, 4, figsize=(16, 5))
# for n,encoding_angle in enumerate(arranged_encoding_angles):
#     subset = combined_df[combined_df['encoding_angle'] == encoding_angle]    
#     ax = axs[n]
#     sns.scatterplot(data=subset, x='location_error_x',y='location_error_z',color=sns.color_palette("dark:#5A9_r")[round(1.7*n)],alpha=0.8,ax=axs[n])
#     ax.plot(0,0,c="#eb8a90",marker="^")
#     ax.set_xlim([-6,6])
#     ax.set_ylim([-6,6]) 
#     ax.set(xlabel='Location Error X',ylabel='Location Error Z', title=f'Encoding Angle {encoding_angle}°')  
# # plt.suptitle(f'Combined Scatterplot of Location Error for Same Encoding Angle',fontsize=16)  
# plt.show()

# location error histogram by 4 encoding distances
fig, axs = plt.subplots(1, 4, figsize=(16, 5))
for n,encoding_distance in enumerate(arranged_encoding_distance):
    subset = combined_df[combined_df['encoding_distance'] == encoding_distance]
    ax = axs[n]
    sns.histplot(data=subset, x='location_error', binwidth=0.2,color=sns.color_palette("dark:#5A9_r")[round(1.7*n)],kde=True, alpha=0.8, element='step',ax=axs[n])
    ax.set_xlim(0,9)
    ax.axvline(x=0,linestyle=":")
    ax.set(xlabel='Locational Error',title=f'Encoding Distance {encoding_distance}m')   
plt.suptitle(f'Combined Histogram of Locational Error for Same Encoding Distance',fontsize=16)  
plt.show()


# location error histograms by encoding angles > 180 or < 180
fig, axs = plt.subplots(1, 2, figsize=(8, 5))
for n,is_reflex_angle in enumerate(arranged_is_reflex):
    subset = combined_df[combined_df['is_reflex_angle'] == is_reflex_angle]    
    ax = axs[n]
    sns.scatterplot(data=subset, x='location_error_x',y='location_error_z',color=sns.color_palette("dark:#5A9_r")[round(1.7*n)],alpha=0.8,ax=axs[n])
    ax.plot(0,0,c="#eb8a90",marker="^")
    ax.set_xlim([-6,6])
    ax.set_ylim([-6,6]) 
    ax.set(xlabel='Location Error X',ylabel='Location Error Z', title=f'>180° {is_reflex_angle}')  
# plt.suptitle(f'Combined Scatterplot of Target Locations',fontsize=16)  
plt.show()





