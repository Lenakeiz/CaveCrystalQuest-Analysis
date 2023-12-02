import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, RegularPolygon
import math

    
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
    
def visualise_ccq_trial(d):

    # a: plot starting corner
    plt.plot(d['startingCorner_x'],d['startingCorner_z'],marker="o",markersize=12, markerfacecolor="green")

    # b: plot standing position in the fog
    plt.plot(d['turningEncodingPosition_x'],d['turningEncodingPosition_z'],marker="o",markersize=12, color="blue")

    # c: plot walking path
    dx = (d['turningEncodingPosition_x'] - d['startingCorner_x']) *0.95
    dz = (d['turningEncodingPosition_z'] - d['startingCorner_z']) *0.95
    plt.arrow(d['startingCorner_x'], d['startingCorner_z'], dx, dz,head_width = 0.1,color="blue",length_includes_head=True)
    
    # d: plot the walking path extending beyond standing point 
    plt.arrow(d['turningEncodingPosition_x'],d['turningEncodingPosition_z'],d['encodingDirection_x'],d['encodingDirection_z'],head_length=None,linestyle=':', color='blue')
    
    # e: plot where crystal is found
    encodingAngle = d['encodingAngle']                  
    if d['isEncodingClockwise'] is False:
        encodingAngle = -encodingAngle 
    originalAngle = math.atan2(d['turningEncodingPosition_z'] - d['startingCorner_z'], d['turningEncodingPosition_x'] - d['startingCorner_x'])
    crystalDirection = originalAngle-math.radians(encodingAngle)
    crystalOrigin_x = d['turningEncodingPosition_x'] + math.cos(crystalDirection)
    crystalOrigin_z = d['turningEncodingPosition_z'] + math.sin(crystalDirection)
    plt.plot(crystalOrigin_x,crystalOrigin_z,marker="d",markersize=9,color="gray",alpha=0.7)

    # f: plot the direction facing where the crystal is found
    plt.plot([d['turningEncodingPosition_x'], crystalOrigin_x], [d['turningEncodingPosition_z'], crystalOrigin_z], linestyle=':', color='gray')
    
    # g: plot where cystal is placed
    plt.plot(d['productionDistance_x'],d['productionDistance_z'],marker="d",markersize=12,color="cyan")

    # h: plot homing direction
    plt.arrow(d['turningEncodingPosition_x'], d['turningEncodingPosition_z'], d['productionDirection_x'], d['productionDirection_z'],head_width = 0.08,color="cyan")

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
    drawCircArrow(ax,1,d['turningEncodingPosition_x'],d['turningEncodingPosition_z'],angle_,theta2_,orientation_,arrowDirection_,color_='grey')
    
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
    drawCircArrow(ap,1.5,d['turningEncodingPosition_x'],d['turningEncodingPosition_z'],angle_,theta2_,orientation_,arrowDirection_,color_='cyan')
    
    plt.xlabel('X position', fontsize=10)
    plt.ylabel('Z position', fontsize=10)
    plt.xlim([-2,2])
    plt.ylim([-2,2])
    plt.title('Trial Route')
    plt.axis('equal')
    plt.show()  
    
data = pd.read_csv('3.csv')
for trial_num in data['sequenceNumber']:
    single_trial = data.iloc[[trial_num]].squeeze().to_dict()   
    visualise_ccq_trial(single_trial)
    
    


