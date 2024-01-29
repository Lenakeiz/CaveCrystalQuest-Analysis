import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, RegularPolygon
import math
from config import color_palette
import os
import re

def drawCircArrow(ax,radius,centX,centY,angle_,theta2_,orientation_,arrowDirection_,color_,linestyle,linewidth = 1.2,label=None):
    
    # Create the arc (circle in this case)
    arc = Arc([centX, centY], radius*2, radius*2, angle=angle_, theta1=0, theta2=theta2_, capstyle='round', linestyle=linestyle, lw=linewidth, color=color_)
    ax.add_patch(arc)
    
    # Create triangle as arrow head (not needed for a full circle, but included as per function definition)
    arrowHead_X = centX + (radius * np.cos(math.radians(arrowDirection_)))
    arrowHead_Y = centY + (radius * np.sin(math.radians(arrowDirection_)))
    arrowHead = RegularPolygon((arrowHead_X, arrowHead_Y), numVertices=3, radius=radius/20, orientation=orientation_, color=color_, linewidth=linewidth, label=label)
    ax.add_patch(arrowHead)

def calculateProductionAngle(productionDirection,crystalDirection,isClockwise):
    if isClockwise:
        # ProductionClockwise 
        angle_ = productionDirection
        theta2_ = math.degrees(crystalDirection) - productionDirection
        orientation_ = math.radians(angle_-180)
        arrowDirection_ = angle_ 
        
    else:
        # ProductionAntiClockwise 
        angle_ = math.degrees(crystalDirection)
        theta2_ = productionDirection - angle_
        orientation_ = math.radians(angle_+theta2_)
        arrowDirection_ = theta2_+angle_  
    return angle_, theta2_, orientation_, arrowDirection_  

def calculateEncodeAngle(encodingAngle,originalAngle,isEncodingClockwise):
    theta2_ = encodingAngle
    if isEncodingClockwise:
        angle_ = originalAngle - encodingAngle
        orientation_ = math.radians(angle_-180)
        arrowDirection_ = angle_
    else:
        angle_ = originalAngle
        orientation_ = math.radians(angle_+theta2_)
        arrowDirection_ = theta2_+angle_
    return angle_,theta2_,orientation_,arrowDirection_    

def drawTheoryTurns(encodingAngle):
    #plotting variables
    line_width= 2
    starting_marker_size = 15
    crystal_marker_size_spawn = 15
    arrow_encoding_distance_color = color_palette[4]
    fog_position_color = color_palette[0]
    encoding_angle_color = color_palette[1]
    production_angle_color = color_palette[2]
    circular_arrow_width = 3.0
    text_font_ticks = 13


    originalAngle = 90
    productionDirection = 270
    isEncodingClockwise = True

    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    
    # a: plot starting corner
    plt.plot(0,-1,marker="o",markersize=10, color=arrow_encoding_distance_color)

    # b: plot standing position in the fog
    plt.plot(0,0,marker="o",markersize=starting_marker_size, color=fog_position_color)

    # d: plot the walking path extending beyond standing point
    plt.plot([0,0], [0,1], lw=line_width, linestyle='--', color=arrow_encoding_distance_color)

    # e: plot where crystal is found                 
    if isEncodingClockwise is False:
        encodingAngle = -encodingAngle 
    crystalDirection = math.radians(originalAngle)-math.radians(encodingAngle)
    crystalOrigin_x = math.cos(crystalDirection)
    crystalOrigin_z = math.sin(crystalDirection)
    plt.plot(crystalOrigin_x,crystalOrigin_z,marker="d",markersize=crystal_marker_size_spawn,color=encoding_angle_color,alpha=1.0)

    # i: plot encoding angle
    angle_,theta2_,orientation_,arrowDirection_ = calculateEncodeAngle(encodingAngle,originalAngle,isEncodingClockwise)
    drawCircArrow(ax,0.55,0,0,angle_,theta2_,orientation_,arrowDirection_,color_=encoding_angle_color,linestyle='-',linewidth=circular_arrow_width, label=f"Encoding Angle {encodingAngle}°")
    

    # f: plot the direction facing where the crystal is found
    plt.plot([0, crystalOrigin_x], [0, crystalOrigin_z], linestyle=':', lw=line_width, color=encoding_angle_color)

    # c: plot homing direction and point
    plt.plot([0,0], [0,-0.9], lw=line_width, linestyle='--', color=production_angle_color)
    plt.plot(0,-0.9,marker="d",markersize=starting_marker_size,color=production_angle_color)

    # #j: plot production angles 
    isClockwise = True
    angle_, theta2_, orientation_, arrowDirection_ = calculateProductionAngle(productionDirection,crystalDirection,isClockwise)
    drawCircArrow(ax,0.6,0,0,angle_,theta2_,orientation_,arrowDirection_,color_=production_angle_color,linestyle='-',linewidth=circular_arrow_width,label=f"Homing Angle 240°")

    # isClockwise = False
    # angle_, theta2_, orientation_, arrowDirection_ = calculateProductionAngle(productionDirection,crystalDirection,isClockwise)
    # drawCircArrow(ax,0.7,0,0,angle_,theta2_,orientation_,arrowDirection_,color_=production_angle_color, linestyle='-',linewidth=circular_arrow_width,label="Homing Angle 240°")
    
    # Set the limits for x-axis and y-axis
    plt.axis('equal')
    plt.axis('off')
    plt.legend(loc='best', fontsize=8) 
    plt.show()



def save_trial_figure(fig, encodingAngle,simulation_dir):
    """
    Saves the given figure to the specified output directory with a filename based on the trial number.

    Parameters:
    fig (matplotlib.figure.Figure): The figure to save.
    trial_num (int): The trial number.
    output_dir (str): The directory where the figure should be saved.
    """
    if not os.path.exists(simulation_dir):
        os.makedirs(simulation_dir)
    fig.savefig(os.path.join(simulation_dir, f'encoding{encodingAngle}.png'))
    plt.close(fig)
 
if __name__ == "__main__":

    # Make sure that you have already the folder data and output created at the same level as this script
    # Getting the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # create output folder
    simulation_dir = os.path.join(script_dir,"trial_simulation") 
    if not os.path.exists(simulation_dir):
        os.makedirs(simulation_dir)  

    encodingAngleList = [300]
    for encodingAngle in encodingAngleList:
        drawTheoryTurns(encodingAngle)