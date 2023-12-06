import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, RegularPolygon
import math
import os

def normalise_angle(angle):
    if angle > 360:
        return angle - 360
    elif angle < 0:
        return angle + 360
    else:
        return angle
   
def drawCircArrow(ax,radius,centX,centY,angle_,theta2_,orientation_,arrowDirection_,color_):
    
    #Create the line   
    arc = Arc([centX,centY],radius,radius,angle=angle_,theta1=0,theta2=theta2_,capstyle='round',linestyle=':',lw=1.2,color=color_)
    ax.add_patch(arc)
    
    #Create triangle as arrow head
    arrowHead_X=centX+(radius/2)*np.cos(math.radians(arrowDirection_)) #Do trig to determine crystalOrigin_ position
    arrowHead_Y=centY+(radius/2)*np.sin(math.radians(arrowDirection_))  
    arrowHead = RegularPolygon((arrowHead_X, arrowHead_Y),numVertices=3,radius=radius/20,orientation=orientation_,color=color_)
    ax.add_patch(arrowHead)
    
    # Make sure you keep the axes scaled or else arrow will distort
    ax.set_xlim([centX-radius,centY+radius]) and ax.set_ylim([centY-radius,centY+radius]) 
    
def visualise_ccq_trial(d,trial_num):
    
    plt.figure(figsize=(10,10))
    # a: plot starting corner
    plt.plot(d['startingCorner_x'],d['startingCorner_z'],marker="o",markersize=12, color=[244/255,232/255,108/255])

    # b: plot walking path
    dx = (d['turningEncodingPosition_x'] - d['startingCorner_x']) *0.95
    dz = (d['turningEncodingPosition_z'] - d['startingCorner_z']) *0.95
    plt.arrow(d['startingCorner_x'], d['startingCorner_z'], dx, dz,head_width = 0.2,lw=2,color=[244/255,232/255,108/255],length_includes_head=True)
    
    # c: plot standing position in the fog
    plt.plot(d['turningEncodingPosition_x'],d['turningEncodingPosition_z'],marker="o",markersize=12, color='green')

    # d: plot the walking path extending beyond standing point 
    plt.arrow(d['turningEncodingPosition_x'],d['turningEncodingPosition_z'],d['encodingDirection_x'],d['encodingDirection_z'],head_length=None,linestyle=':', color='green')
    
    # e: plot where crystal is found
    encodingAngle = d['encodingAngle']                  
    if d['isEncodingClockwise'] is False:
        encodingAngle = -encodingAngle 
    originalAngle = math.atan2(d['turningEncodingPosition_z'] - d['startingCorner_z'], d['turningEncodingPosition_x'] - d['startingCorner_x'])
    crystalDirection = originalAngle-math.radians(encodingAngle)
    crystalOrigin_x = d['turningEncodingPosition_x'] + math.cos(crystalDirection)
    crystalOrigin_z = d['turningEncodingPosition_z'] + math.sin(crystalDirection)
    plt.plot(crystalOrigin_x,crystalOrigin_z,marker="d",markersize=9,color="blue",alpha=0.7)

    # f: plot the direction facing where the crystal is found
    plt.plot([d['turningEncodingPosition_x'], crystalOrigin_x], [d['turningEncodingPosition_z'], crystalOrigin_z], linestyle=':', color='blue')
    
    # g: plot homing direction
    plt.arrow(d['turningEncodingPosition_x'], d['turningEncodingPosition_z'], d['productionDirection_x'], d['productionDirection_z'],head_width = 0.2,lw=2,color='purple')
    
    # h: plot where cystal is placed
    plt.plot(d['productionDistance_x'],d['productionDistance_z'],marker="d",markersize=16,color='purple')
    
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
    ax = plt.gca()
    drawCircArrow(ax,1,d['turningEncodingPosition_x'],d['turningEncodingPosition_z'],angle_,theta2_,orientation_,arrowDirection_,color_='green')
    
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
    ap = plt.gca()
    drawCircArrow(ap,1.5,d['turningEncodingPosition_x'],d['turningEncodingPosition_z'],angle_,theta2_,orientation_,arrowDirection_,color_='blue')
     
    plt.xlabel('X Position', fontsize=10)
    plt.ylabel('Z Position', fontsize=10)
    plt.axis('equal')
    plt.title(f'Trial {trial_num} Route')
    plt.savefig(f'../trial_graph/subj{subjid}_trial{trial_num}.png')
    plt.close()
    return theta2_

def calculate_error(d,theta2_):
    # k: calculate linear and angular error
    encoding_distance = d['encodingDistance']   
    production_distance = np.sqrt((d['productionDistance_x'] - d['turningEncodingPosition_x'])**2 + (d['productionDistance_z'] - d['turningEncodingPosition_z'])**2)
    linear_error = (production_distance - encoding_distance)/encoding_distance
    
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
    angular_error = (production_angle - homing_angle)/homing_angle
    trial_error = [encoding_angle, homing_angle, np.round(production_angle,3), np.round(angular_error,3), encoding_distance,np.round(production_distance,3), np.round(linear_error,3)]
    return trial_error
    # print(f"Trial the encoding_angle is {encoding_angle}, the homing_angle is {homing_angle}, the production_angle is {production_angle}, the angular error is {angular_error:3f}. the encoding distance is {encoding_distance:3f}, the production distance is {production_distance:3f}, the linear error is {linear_error:3f}")

    
subjid = input("Enter the participant ID: ")
data = pd.read_csv(os.path.abspath(f"../data/{subjid}.csv"))
error_stats = pd.DataFrame(columns=['encoding_angle', 'homing_angle', 'production_angle', 'angular_error', 'encoding_distance','production_distance', 'linear_error'])

for trial_num in data['sequenceNumber']:
    single_trial = data.iloc[[trial_num-1]].squeeze().to_dict()   
    theta2_ = visualise_ccq_trial(single_trial,trial_num)
    trial_error = calculate_error(single_trial,theta2_)
    new_trial_error = pd.DataFrame([trial_error], columns=error_stats.columns)
    error_stats = pd.concat([error_stats, new_trial_error], ignore_index=True)
    error_stats.to_csv(f'../error_stats/error{subjid}.csv')
    
    
    


