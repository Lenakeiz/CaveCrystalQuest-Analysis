import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

def plot_arc(ax, radius, centX, centY, starting_angle_radians, final_angle_radians, color_='r', linewidth=1.2, label=None):
    # Generate the arc
    arc_angles = np.linspace(starting_angle_radians, final_angle_radians, num=100)
    arc_xs = radius * np.cos(arc_angles) + centX
    arc_ys = radius * np.sin(arc_angles) + centY

    # Draw the arc
    ax.plot(arc_xs, arc_ys, color=color_, linewidth=linewidth, label=label)

    # Calculate the tangent vector at the end of the arc
    tangent_vector = np.array([arc_xs[-1] - arc_xs[-2], arc_ys[-1] - arc_ys[-2]])
    tangent_angle = np.arctan2(tangent_vector[1], tangent_vector[0])

    # Adjust orientation to make the triangle point rightwards along the x-axis
    orientation = tangent_angle - np.pi / 2

    # Regular Polygon takes the circumscribed radius, so we are setting these properties accordingly
    triangle_circumscribed_radius = radius / 20

    # Calculate the new center of the triangle by moving back along the tangent
    triangle_center_x = arc_xs[-1] - triangle_circumscribed_radius * np.cos(tangent_angle)
    triangle_center_y = arc_ys[-1] - triangle_circumscribed_radius * np.sin(tangent_angle) 

    # Create the arrowhead with the new center
    arrowHead = RegularPolygon((triangle_center_x, triangle_center_y), numVertices=3, radius=triangle_circumscribed_radius, orientation=orientation, color=color_)
    ax.add_patch(arrowHead)