import numpy as np
import matplotlib.pyplot as plt

def vis_keep_layer(keep_matrix, contours=[]):
    # Create a figure and axes for plotting
    fig, ax = plt.subplots()
    
    # Visualize the array
    ax.imshow(keep_matrix, cmap='gray', interpolation='nearest')  # 'gray' colormap for black and white, added 'nearest' for sharper image
    
    # Iterate through each contour and plot it on the same axes
    for contour in contours:
        # Plot the exterior of the contour
        x, y = contour.exterior.xy
        ax.plot(x, y, 'r')  # Optional: specify color or other plot properties
        ax.fill(x, y, alpha=0.5)  # Fill the contour for better visibility
    
    # Show the plot
    plt.show()
