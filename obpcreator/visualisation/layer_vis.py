import numpy as np
import matplotlib.pyplot as plt

def vis_keep_layer(keep_matrix):
    # Visualize the array
    plt.imshow(keep_matrix, cmap='gray')  # 'gray' colormap for black and white
    plt.colorbar()  # Optional: adds a colorbar to the side
    plt.show()
