import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt


def arrange_array(arr):
    sorted_arr = np.sort(arr)
    arranged_arr = np.array([sorted_arr[0], 360 - sorted_arr[0], sorted_arr[1], 360 - sorted_arr[1]])
    return arranged_arr

# from plot_trial_route generate production error csv file
folder_path = os.path.join(os.path.dirname(__file__),'output/error_stats') # Replace with the path to your folder
all_files = os.listdir(folder_path)


# same encoding angle 
# Read each file and append its data to the list
for file in all_files:
    if file.endswith('.csv'):
        file_path = os.path.join(folder_path, file)
        combined_df = pd.read_csv(file_path)
        fig, axs = plt.subplots(1, 4, figsize=(20, 5),subplot_kw={'projection': 'polar'})
        arranged_homing_angles = arrange_array(combined_df['encoding_angle'].unique())
        for n,encoding_angle in enumerate(arranged_encoding_angles):
            subset = combined_df[combined_df['encoding_angle'] == encoding_angle]
            ax = axs[n]
            num_bins = 72
            bins = np.linspace(0,2*np.pi, num_bins + 1) # polar histogram default range is 0 to 2 pi
            # Histogram data
            homing_angles = np.sort(subset['homing_angle'].unique()) 
            subset['angular_difference'] = subset['production_angle'] - subset['homing_angle'] +180
            df1 = subset[subset['homing_angle'] == homing_angles[0]]['angular_difference']
            df2 = subset[subset['homing_angle'] == homing_angles[1]]['angular_difference']
            hist1, _ = np.histogram(np.radians(df1), bins)
            hist2, _ = np.histogram(np.radians(df2), bins)

            # Bin width
            width = bins[1] - bins[0]

            # Plotting the bars
            ax.bar(bins[:-1], hist1, width=width, alpha=0.7, color='blue', label=f'Homing Angle {homing_angles[0]}°')
            ax.bar(bins[:-1], hist2, width=width, alpha=0.7, color='orange', label=f'Homing Angle {homing_angles[1]}°')

            # Customizations
            ax.set_theta_zero_location('S')  # Set 0 degrees at the top
            ax.set_theta_direction(-1)       # Clockwise
            ax.set_xticklabels([f"{x}°" for x in range(-180, 180, int(360/num_bins)*9)])
            ax.set_title('Production Angle Distribution by Homing Angle', va='bottom')
            ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))
            ax.set(xlabel='Angular Production Error ',title=f'Encoding Angle {encoding_angle}°')   
        plt.suptitle(f'Combined Histogram of Angular Production for Same Encoding Angle and Different Homing Angles',fontsize=16)  
        plt.show()


# same homing angle 
for file in all_files:
    if file.endswith('.csv'):
        file_path = os.path.join(folder_path, file)
        combined_df = pd.read_csv(file_path)
        fig, axs = plt.subplots(1, 4, figsize=(20, 5),subplot_kw={'projection': 'polar'})
        arranged_homing_angles = arrange_array(combined_df['homing_angle'].unique())
        for n,homing_angle in enumerate(arranged_homing_angles):
            subset = combined_df[combined_df['homing_angle'] == homing_angle]
            ax = axs[n]
            num_bins = 72
            bins = np.linspace(0,2*np.pi, num_bins + 1) # polar histogram default range is 0 to 2 pi
            # Histogram data
            encoding_angles = np.sort(subset['encoding_angle'].unique()) 
            subset['angular_difference'] = subset['production_angle'] - subset['homing_angle'] +180
            df1 = subset[subset['encoding_angle'] == encoding_angles[0]]['angular_difference']
            df2 = subset[subset['encoding_angle'] == encoding_angles[1]]['angular_difference']
            hist1, _ = np.histogram(np.radians(df1), bins)
            hist2, _ = np.histogram(np.radians(df2), bins)

            # Bin width
            width = bins[1] - bins[0]

            # Plotting the bars
            ax.bar(bins[:-1], hist1, width=width, alpha=0.7, color='blue', label=f'encoding Angle {encoding_angles[0]}°')
            ax.bar(bins[:-1], hist2, width=width, alpha=0.7, color='orange', label=f'encoding Angle {encoding_angles[1]}°')

            # Customizations
            ax.set_theta_zero_location('S')  # Set 0 degrees at the top
            ax.set_theta_direction(-1)       # Clockwise
            ax.set_xticklabels([f"{x}°" for x in range(-180, 180, int(360/num_bins)*9)])
            ax.set_title('Production Angle Distribution by encoding Angle', va='bottom')
            ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5))
            ax.set(xlabel='Angular Production Error ',title=f'Homing Angle {homing_angle}°')   
        plt.suptitle(f'Combined Histogram of Angular Production for Same homing Angle and Different Encoding Angles',fontsize=16)  
        plt.show()

