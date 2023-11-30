import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation,PillowWriter
from matplotlib.patches import Arc, RegularPolygon
import math


def drawCircArrow(ax,radius,centX,centY,angle_,theta2_,orientation_,arrowDirection_,color_):
    
    #Create the line   
    arc = Arc([centX,centY],radius,radius,angle=angle_,theta1=0,theta2=theta2_,capstyle='round',linestyle=':',lw=1.5,color=color_)
    ax.add_patch(arc)
    
    #Create triangle as arrow head
    arrowHead_X=centX+(radius/2)*np.cos(math.radians(arrowDirection_)) #Do trig to determine crystalOrigin_ position
    arrowHead_Y=centY+(radius/2)*np.sin(math.radians(arrowDirection_))  
    arrowHead = RegularPolygon((arrowHead_X, arrowHead_Y),numVertices=3,radius=radius/15,orientation=orientation_,color=color_)
    ax.add_patch(arrowHead)
    
    # Make sure you keep the axes scaled or else arrow will distort
    ax.set_xlim([centX-radius,centY+radius]) and ax.set_ylim([centY-radius,centY+radius]) 
    
def visualise_ccq_trial(d):

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
    plt.xlim([-3,3])
    plt.ylim([-3,3])
    plt.title('Trial Route')

def animate(i):
    tmp = st_tracking.iloc[:i,:]
    tmp_q = st_tracking.iloc[i-1:i,:]
    ax.clear()
    ax.set_xlabel('X Position', fontsize=10)
    ax.set_ylabel('Z Position', fontsize=10)
    ax.set_title('Trial Motion')
    ax.set_xlim([-3,3])
    ax.set_ylim([-3,3])
    scat = ax.scatter(tmp['position_x'], tmp['position_z'], c=tmp['timestamp'],cmap='viridis_r')
    quiv = ax.quiver(tmp_q['position_x'],tmp_q['position_z'],
                      tmp_q['normdir_x'],tmp_q['normdir_z'],
                      color='purple',headwidth=4,headlength=4,headaxislength=3,scale=30)
    
    return scat,quiv

data = pd.read_csv('data/0000.csv')
data_tracking = pd.read_csv('data/0000_tracking.csv')
data_tracking['norm_vector'] = np.sqrt(1/(data_tracking['forward_x']**2+data_tracking['forward_z']**2))
data_tracking['normdir_x'] = data_tracking['forward_x']*data_tracking['norm_vector']
data_tracking['normdir_z'] = data_tracking['forward_z']*data_tracking['norm_vector']
for trial_num in data_tracking['sequenceNumber'].unique(): 
    st_tracking = data_tracking[data_tracking['sequenceNumber']==trial_num]
    single_trial = data[data['sequenceNumber']==trial_num].squeeze().to_dict() 
    t_start = single_trial['timeAtStartEncodingDistance']
    t_end = single_trial['timeAtEndProductionDistance']
    st_tracking = st_tracking[st_tracking['timestamp'].between(t_start,t_end)]    
    fig = plt.figure(figsize=(12,5))

    ax = fig.add_subplot(121)
    scat = ax.scatter([], [], [])
    quiv = ax.quiver([],[],[],[])
    anim = FuncAnimation(fig, animate, frames=2000, interval=100, repeat=False)
    fig.add_subplot(122)
    visualise_ccq_trial(single_trial) 
    plt.show()
    #anim.save(f'3_{trial_num}.gif', writer=PillowWriter(fps=10))
    print(t_start,t_end)
    print(st_tracking)

