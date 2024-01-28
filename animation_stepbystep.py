import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation,PillowWriter
from matplotlib.patches import Arc, RegularPolygon
from config import folder_names,color_palette
import math
import os
import re

starting_position_color = color_palette[4]
arrow_encoding_distance_color = color_palette[4]
fog_position_color = color_palette[0]
encoding_angle_color = color_palette[1]
production_angle_color = color_palette[2]

def drawCircArrow(ax,radius,centX,centY,angle_,theta2_,orientation_,arrowDirection_,color_):
    
    #Create the line   
    arc = Arc([centX,centY],radius,radius,angle=angle_,theta1=0,theta2=theta2_,capstyle='round',linestyle=':',lw=1.5,color=color_)
    ax.add_patch(arc)
    
    #Create triangle as arrow head
    arrowHead_X=centX+(radius/2)*np.cos(math.radians(arrowDirection_)) #Do trig to determine crystalOrigin_ position
    arrowHead_Y=centY+(radius/2)*np.sin(math.radians(arrowDirection_))  
    arrowHead = RegularPolygon((arrowHead_X, arrowHead_Y),numVertices=3,radius=radius/15,orientation=orientation_,color=color_)
    ax.add_patch(arrowHead)
    ax.set_xlim([centX-radius,centY+radius]) and ax.set_ylim([centY-radius,centY+radius]) 


def add_route(d_tracking,d,ax): 
    
    originalAngle = math.atan2(d['turningEncodingPosition_z'] - d['startingCorner_z'], d['turningEncodingPosition_x'] - d['startingCorner_x'])
    encodingAngle = d['encodingAngle']                  
    if d['isEncodingClockwise'] is False:
        encodingAngle = -encodingAngle 
    crystalDirection = originalAngle-math.radians(encodingAngle)
    
    if d_tracking['timestamp'] > d['timeAtStartEncodingDistance']:
        # a: plot starting corner
        plt.plot(d['startingCorner_x'],d['startingCorner_z'],marker="o",markersize=8, color=color_palette[4])
    if d_tracking['timestamp'] > d['timeAtStartEncodingAngle']:   
        # c: plot standing position in the fog
        plt.plot(d['turningEncodingPosition_x'],d['turningEncodingPosition_z'],marker="o",markersize=8, color=fog_position_color)

        # d: plot the walking path extending beyond standing point 
        plt.arrow(d['turningEncodingPosition_x'],d['turningEncodingPosition_z'],d['encodingDirection_x'],d['encodingDirection_z'],head_length=None,linestyle=':', color=arrow_encoding_distance_color)
    
    if d_tracking['timestamp'] > d['timeAtEndEncodingAngle']: 
        # i: plot encoding angle
        theta2_ = d['encodingAngle']
        if d['isEncodingClockwise']:
            angle_ = math.degrees(originalAngle) - d['encodingAngle']
            orientation_ = math.radians(angle_-180)
            arrowDirection_ = angle_
        else:
            angle_ = math.degrees(originalAngle)
            orientation_ = math.radians(angle_+theta2_)
            arrowDirection_ = theta2_+angle_
        ap = plt.gca()
        drawCircArrow(ap,1,d['turningEncodingPosition_x'],d['turningEncodingPosition_z'],angle_,theta2_,orientation_,arrowDirection_,color_=encoding_angle_color)
    
    if d_tracking['timestamp'] > d['timeAtStartProductionAngle']: 
        # e: plot where crystal is found
        
        crystalOrigin_x = d['turningEncodingPosition_x'] + math.cos(crystalDirection)
        crystalOrigin_z = d['turningEncodingPosition_z'] + math.sin(crystalDirection)
        plt.plot(crystalOrigin_x,crystalOrigin_z,marker="d",markersize=9,color=encoding_angle_color,alpha=0.9)

        # f: plot the direction facing where the crystal is found
        plt.plot([d['turningEncodingPosition_x'], crystalOrigin_x], [d['turningEncodingPosition_z'], crystalOrigin_z], linestyle=':', color=encoding_angle_color)
    
    if d_tracking['timestamp'] > d['timeAtEndProductionAngle']:
        # j: plot production angle    
        productionDirection = math.degrees(math.atan2(d['productionDirection_z'],d['productionDirection_x']))
        if d['isProductionClockwise']:
            angle_ = productionDirection
            theta2_ = math.degrees(crystalDirection) - productionDirection
            orientation_ = math.radians(angle_-180)
            arrowDirection_ = angle_ 
        else:
            angle_ = math.degrees(crystalDirection)
            theta2_ = productionDirection - angle_
            orientation_ = math.radians(angle_+theta2_)
            arrowDirection_ = theta2_+angle_         
        aq = plt.gca()
        drawCircArrow(aq,1.5,d['turningEncodingPosition_x'],d['turningEncodingPosition_z'],angle_,theta2_,orientation_,arrowDirection_,color_=production_angle_color)
    
    if d_tracking['timestamp'] > d['timeAtStartProductionDistance']:
        # g: plot homing direction
        plt.arrow(d['turningEncodingPosition_x'], d['turningEncodingPosition_z'], d['productionDirection_x'], d['productionDirection_z'],head_width = 0.2,lw=2,color=production_angle_color)
        # h: plot where cystal is placed
        plt.plot(d['productionDistance_x'],d['productionDistance_z'],marker="d",markersize=16,color=production_angle_color)
    plt.xlabel('X Position', fontsize=10)
    plt.ylabel('Z Position', fontsize=10)
    plt.xlim([-3,3])
    plt.ylim([-3,3])
    plt.title(f'Trial {trial_num} Route')  

    
        
def animate(i):
    tmp = st_tracking.iloc[:i,:]
    tmp_q = st_tracking.iloc[i,:]   
    
    ax.clear()
    ax.set_xlabel('X Position', fontsize=10)
    ax.set_ylabel('Z Position', fontsize=10)
    ax.set_title(f'Trial {trial_num} Motion')
    ax.set_xlim([-3,3])
    ax.set_ylim([-3,3])
      
    scat = plt.scatter(tmp['position_x'], tmp['position_z'], c=tmp['timestamp'],cmap='Reds',alpha=0.7)
    quiv = plt.quiver(tmp_q['position_x'],tmp_q['position_z'],
                      tmp_q['normdir_x'],tmp_q['normdir_z'],
                      color='purple',headwidth=8,headlength=8,headaxislength=5,scale=20)
    rout = add_route(tmp_q,single_trial,ax)
    return scat,quiv,rout,


def normalise_angle(angle):
    if angle >= 360:
        return angle - 360
    elif angle < 0:
        return angle + 360
    else:
        return angle

if __name__ == "__main__":

    # Make sure that you have already the folder data and output created at the same level as this script
    # Getting the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # create output folder
    base_output_dir = os.path.join(script_dir,"output/trial_animation")
    base_input_dir = os.path.join(script_dir,"data")
    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)
    
    for folder_name in folder_names:
        
        # create an input folder path specific for this category of people
        input_folder_path = os.path.join(base_input_dir, folder_name)
        # create an output folder specific for this category of people
        output_dir = os.path.join(base_output_dir, folder_name)

        if not os.path.exists(input_folder_path):
            print(f"Input folder {input_folder_path} does not exist. Skipping...")
            continue
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)  
        
        # processing files in the directory:
        for file in os.listdir(input_folder_path):
            if re.match(r"^\d+\.csv$", file):
                subjid = file.split('.')[0]
                subjid = re.match(r"^\d+", file).group(0)
                subj_output_dir = os.path.join(output_dir, subjid)
                
                # creating a folder output for the participant
                if not os.path.exists(subj_output_dir):
                    os.makedirs(subj_output_dir)

                data_path = os.path.join(input_folder_path, file)
                data = pd.read_csv(data_path)
                data_tracking_path = os.path.join(input_folder_path, f'{subjid}_tracking.csv')
                data_tracking = pd.read_csv(data_tracking_path)
                data_tracking['norm_vector'] = np.sqrt(1/(data_tracking['forward_x']**2+data_tracking['forward_z']**2))
                data_tracking['normdir_x'] = data_tracking['forward_x']*data_tracking['norm_vector']
                data_tracking['normdir_z'] = data_tracking['forward_z']*data_tracking['norm_vector']

                for trial_num in data_tracking['sequenceNumber'].unique(): 
                    print(f'Generating animation for trial {trial_num} of participant {subjid}...')
                    st_tracking = data_tracking[data_tracking['sequenceNumber']==trial_num]
                    single_trial = data[data['sequenceNumber']==trial_num].squeeze().to_dict() 
                    # route between start walking and finish pointing
                    t_start = single_trial['timeAtStartEncodingDistance']
                    t_end = single_trial['timeAtEndProductionDistance']
                    st_tracking = st_tracking[st_tracking['timestamp'].between(t_start,t_end)]    
                    fig = plt.figure(figsize=(7,7))
                    ax = fig.add_subplot(111)
                    scat = ax.scatter([], [], [])
                    quiv = ax.quiver([],[],[],[])
                    rout = ax.plot(single_trial['startingCorner_x'],single_trial['startingCorner_z'],marker="o",markersize=8, color=color_palette[4])
                    anim = FuncAnimation(fig, animate, frames=len(st_tracking), interval=1, repeat=False) #frames: length of animation, interval: time between fram n-1 and n
                    anim.save(os.path.join(subj_output_dir,f'trial_{trial_num}.gif'), writer=PillowWriter(fps=30))
                    # plt.show()

