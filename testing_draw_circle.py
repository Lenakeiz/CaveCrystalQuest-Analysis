import matplotlib.pyplot as plt
from matplotlib.patches import Arc, RegularPolygon
import math
import numpy as np

def drawCircArrow(ax, radius, centX, centY, angle_, theta2_, orientation_, arrowDirection_, color_, linewidth=1.2):
    # Create the arc (circle in this case)
    arc = Arc([centX, centY], radius*2, radius*2, angle=angle_, theta1=0, theta2=theta2_, capstyle='round', linestyle='-', lw=linewidth, color=color_)
    ax.add_patch(arc)
    
    # Create triangle as arrow head (not needed for a full circle, but included as per function definition)
    arrowHead_X = centX + (radius * np.cos(math.radians(arrowDirection_)))
    arrowHead_Y = centY + (radius * np.sin(math.radians(arrowDirection_)))
    arrowHead = RegularPolygon((arrowHead_X, arrowHead_Y), numVertices=3, radius=radius/20, orientation=orientation_, color=color_, edgecolor='black', linewidth=linewidth)
    ax.add_patch(arrowHead)

# Create a figure and axis
fig, ax = plt.subplots()

# Parameters for the circle
radius = 1
center_x = 1
center_y = 1
angle_ = 0
theta2_ = 360  # Full circle
orientation_ = 0
arrowDirection_ = 90  # Direction where the arrow head points
color_ = "blue"

# Draw a circle
drawCircArrow(ax, radius, center_x, center_y, angle_, theta2_, orientation_, arrowDirection_, color_)

# Set axis limits to properly display the circle
ax.set_xlim(0, 2)
ax.set_ylim(0, 2)
ax.set_aspect('equal', 'box')  # Ensures circle is not distorted

plt.show()
