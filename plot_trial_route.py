import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, RegularPolygon
import math
import os
import re

from config import folder_names
from config import color_palette

def normalise_angle(angle):
    if angle > 720:
        return angle - 720
    if angle > 360 and angle < 720:
        return angle - 360
    if angle < 0 and angle > -360:
        return angle + 360
    elif angle < -360:
        return angle + 720
    else:
        return angle
   
def drawCircArrow(ax,radius,centX,centY,angle_,theta2_,orientation_,arrowDirection_,color_,linewidth = 1.2,label=None):
    
    # Create the arc (circle in this case)
    arc = Arc([centX, centY], radius*2, radius*2, angle=angle_, theta1=0, theta2=theta2_, capstyle='round', linestyle='-', lw=linewidth, color=color_)
    ax.add_patch(arc)
    
    # Create triangle as arrow head (not needed for a full circle, but included as per function definition)
    arrowHead_X = centX + (radius * np.cos(math.radians(arrowDirection_)))
    arrowHead_Y = centY + (radius * np.sin(math.radians(arrowDirection_)))
    arrowHead = RegularPolygon((arrowHead_X, arrowHead_Y), numVertices=3, radius=radius/20, orientation=orientation_, color=color_, linewidth=linewidth, label=label)
    ax.add_patch(arrowHead)
    
    # Make sure you keep the axes scaled or else arrow will distort
    #ax.set_xlim([centX-radius,centY+radius]) and ax.set_ylim([centY-radius,centY+radius]) 
    
def visualise_ccq_trial(d,trial_num):
    
    #plotting variables
    head_width = 0.1
    line_width= 2
    starting_marker_size = 12
    crystal_marker_size_spawn = 15
    crystal_marker_size_reposition = 15
    starting_position_color = color_palette[4]
    arrow_encoding_distance_color = color_palette[4]
    fog_position_color = color_palette[0]
    encoding_angle_color = color_palette[1]
    production_angle_color = color_palette[2]
    circular_arrow_width = 3.0
    text_font_size = 16
    text_font_ticks = 13
    text_font_size_title = 19


    plt.figure(figsize=(10,10))
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')  # Ensures circles are not distorted

    # a: plot starting corner
    plt.plot(d['startingCorner_x'],d['startingCorner_z'],marker="o",markersize=starting_marker_size, color=arrow_encoding_distance_color)    
    
    # b: plot walking path
    dx = (d['turningEncodingPosition_x'] - d['startingCorner_x']) *1.0
    dz = (d['turningEncodingPosition_z'] - d['startingCorner_z']) *1.0
    plt.arrow(d['startingCorner_x'], d['startingCorner_z'], dx, dz,head_width = head_width,lw=line_width,color=arrow_encoding_distance_color,length_includes_head=True, label="Encoding Distance")
    
    # b: plot standing position in the fog
    plt.plot(d['turningEncodingPosition_x'],d['turningEncodingPosition_z'],marker="o",markersize=starting_marker_size, color=fog_position_color)
   
    # d: plot the walking path extending beyond standing point
    start_x = d['turningEncodingPosition_x']
    start_z = d['turningEncodingPosition_z']
    end_x = start_x + d['encodingDirection_x']
    end_z = start_z + d['encodingDirection_z']
    plt.plot([start_x, end_x], [start_z, end_z], lw=line_width, linestyle='--', color=arrow_encoding_distance_color)
    
    # e: plot where crystal is found
    encodingAngle = d['encodingAngle']                  
    if d['isEncodingClockwise'] == False:
        encodingAngle = -encodingAngle 
    originalAngle = math.atan2(d['turningEncodingPosition_z'] - d['startingCorner_z'], d['turningEncodingPosition_x'] - d['startingCorner_x'])
    crystalDirection = originalAngle-math.radians(encodingAngle)
    crystalOrigin_x = d['turningEncodingPosition_x'] + math.cos(crystalDirection)
    crystalOrigin_z = d['turningEncodingPosition_z'] + math.sin(crystalDirection)
    
    # i: plot encoding angle
    theta2_ = d['encodingAngle']
    if d['isEncodingClockwise'] == True:
        angle_ = math.degrees(originalAngle) - d['encodingAngle']
        orientation_ = math.radians(angle_-180)
        arrowDirection_ = angle_
    else:
        angle_ = math.degrees(originalAngle)
        orientation_ = math.radians(angle_+theta2_)
        arrowDirection_ = theta2_+angle_
    drawCircArrow(ax,0.5,d['turningEncodingPosition_x'],d['turningEncodingPosition_z'],angle_,theta2_,orientation_,arrowDirection_,color_=encoding_angle_color, linewidth=circular_arrow_width, label="Encoding Angle")
    
    # j: plot production angle    
    productionDirection = math.degrees(math.atan2(d['productionDirection_z'],d['productionDirection_x']))
    if d['isProductionClockwise'] == True:
        angle_ = productionDirection
        theta2_ = math.degrees(crystalDirection) - productionDirection
        orientation_ = math.radians(angle_-180)
        arrowDirection_ = angle_ 
    else:
        angle_ = math.degrees(crystalDirection)
        theta2_ = productionDirection - angle_
        orientation_ = math.radians(angle_+theta2_)
        arrowDirection_ = theta2_+angle_         
    drawCircArrow(ax,1.0,d['turningEncodingPosition_x'],d['turningEncodingPosition_z'],angle_,theta2_,orientation_,arrowDirection_,color_=production_angle_color, linewidth=circular_arrow_width, label="Production Angle")
    
    plt.plot(crystalOrigin_x,crystalOrigin_z,marker="d",markersize=crystal_marker_size_spawn,color=encoding_angle_color,alpha=1.0)

    # f: plot the direction facing where the crystal is found
    plt.plot([d['turningEncodingPosition_x'], crystalOrigin_x], [d['turningEncodingPosition_z'], crystalOrigin_z], linestyle=':', lw=line_width, color=encoding_angle_color)

    # g: plot homing direction
    start_x = d['turningEncodingPosition_x']
    start_z = d['turningEncodingPosition_z']
    end_x = start_x + d['productionDirection_x']
    end_z = start_z + d['productionDirection_z']
    plt.plot([d['turningEncodingPosition_x'], d['productionDistance_x']], [d['turningEncodingPosition_z'], d['productionDistance_z']], lw=line_width, linestyle='--', color=production_angle_color, label="Production Distance")
 
    # h: plot where cystal is placed
    plt.plot(d['productionDistance_x'],d['productionDistance_z'],marker="d",markersize=crystal_marker_size_reposition,color=production_angle_color)
         
    # Set the limits for x-axis and y-axis
    plt.xlim(-3, 3)
    plt.ylim(-3, 3)
    plt.xlabel('X Position', fontsize=text_font_size)
    plt.ylabel('Z Position', fontsize=text_font_size)
    plt.xticks(fontsize=text_font_ticks)
    plt.yticks(fontsize=text_font_ticks)
    plt.axis('equal')

    plt.legend(loc='best', fontsize=text_font_ticks)

    plt.title(f'Trial {trial_num}', fontsize=text_font_size_title)
    
    return theta2_

def calculate_error(d,theta2_,subjid,trial_num):
    # k: calculate linear and angular error
    encoding_distance = d['encodingDistance']   
    production_distance = np.sqrt((d['productionDistance_x'] - d['turningEncodingPosition_x'])**2 + (d['productionDistance_z'] - d['turningEncodingPosition_z'])**2)
    linear_error = production_distance - encoding_distance
    prop_linear_error = production_distance/encoding_distance
    location_error = np.sqrt((d['productionDistance_x'] - d['startingCorner_x'])**2 + (d['productionDistance_z'] - d['startingCorner_z'])**2)
    
    encoding_angle = d['encodingAngle']

    if d['encodingAngle'] < 180:
        if d['isEncodingClockwise'] == d['isProductionClockwise']:
            homing_angle = 180 - encoding_angle
        else:
            homing_angle = 180 + encoding_angle
    else:
        if d['isEncodingClockwise'] == d['isProductionClockwise']:
            homing_angle = 540 - encoding_angle
        else:
            homing_angle = encoding_angle - 180

    production_angle = normalise_angle(theta2_) 
    angular_error = production_angle - homing_angle
    prop_angular_error = production_angle / homing_angle
    trial_error = [subjid, trial_num, encoding_angle, homing_angle, np.round(production_angle,3), np.round(angular_error,3), encoding_distance,np.round(production_distance,3), np.round(linear_error,3),np.round(location_error,3),np.round(prop_angular_error,3),np.round(prop_linear_error,3),d['startingCorner_x'],d['startingCorner_z'],d['productionDistance_x'],d['productionDistance_z']]
    return trial_error
    # print(f"Trial the encoding_angle is {encoding_angle}, the homing_angle is {homing_angle}, the production_angle is {production_angle}, the angular error is {angular_error:3f}. the encoding distance is {encoding_distance:3f}, the production distance is {production_distance:3f}, the linear error is {linear_error:3f}")

def save_trial_figure(fig, trial_num, output_dir):
    """
    Saves the given figure to the specified output directory with a filename based on the trial number.

    Parameters:
    fig (matplotlib.figure.Figure): The figure to save.
    trial_num (int): The trial number.
    output_dir (str): The directory where the figure should be saved.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    fig.savefig(os.path.join(output_dir, f'trial_{trial_num}.png'))
    plt.close(fig)

if __name__ == "__main__":

    # Make sure that you have already the folder data and output created at the same level as this script
    # Getting the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # create output folder
    base_output_dir = os.path.join(script_dir,"output/trial_visualization")
    base_input_dir = os.path.join(script_dir,"data")
    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)
    
    error_dir = os.path.join(script_dir,"output/error_stats")
    if not os.path.exists(error_dir):
            os.makedirs(error_dir)
    
    for folder_name in folder_names:
        # create an input folder path specific for this category of people
        input_folder_path = os.path.join(base_input_dir, folder_name)
        # create an output folder specific for this category of people
        output_dir = os.path.join(base_output_dir, folder_name)

        if not os.path.exists(input_folder_path):
            print(f"Input folder {input_folder_path} does not exist. Skipping...")
            continue
        
        print(f"Processing folder {input_folder_path}...")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)        
        
        # processing files in the directory:
        for file in os.listdir(input_folder_path):
            # Regular expression to match the file name
            if re.match(r"^\d+\.csv$", file):
                subjid = file.split('.')[0]
                subjid = re.match(r"^\d+", file).group(0)
                subj_output_dir = os.path.join(output_dir, subjid)
                
                # creating a folder output for the participant
                if not os.path.exists(subj_output_dir):
                    os.makedirs(subj_output_dir)

                data_path = os.path.join(input_folder_path, file)
                data = pd.read_csv(os.path.join(data_path))

                # creating a dataframe to store the calculated metrics
                error_stats = pd.DataFrame(columns=['subject_id','trial_number','encoding_angle', 'homing_angle', 'production_angle', 'angular_error', 'encoding_distance','production_distance', 'linear_error','location_error','prop_angular_error','prop_linear_error','start_position_x','start_position_z','target_position_x','target_position_z'])

                for trial_num in data['sequenceNumber']:

                    print(f"Processing trial {trial_num} for participant {subjid}...")

                    single_trial = data.iloc[[trial_num-1]].squeeze().to_dict()   
                    theta2_ = visualise_ccq_trial(single_trial,trial_num)
                    # Get the current figure and save it
                    fig = plt.gcf()
                    save_trial_figure(fig, trial_num, subj_output_dir)
                    # calculate production error for each trial and save it to error_stats folder
                    trial_error = calculate_error(single_trial,theta2_,subjid,trial_num)
                    new_trial_error = pd.DataFrame([trial_error], columns=error_stats.columns)
                    error_stats = pd.concat([error_stats, new_trial_error], ignore_index=True)
                    
                # save error statistics and run plot_error_distribution.py next
                error_stats.to_csv(os.path.join(error_dir, f'error_{subjid}.csv'))
    
    


