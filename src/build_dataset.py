import os
import sys 
import cv2
import random
import numpy as np
import csv


# Function to generate a random circle or ellipse
def draw_random_shape(image):
    height, width = image.shape[:2]
    shape_type = random.choice(['circle', 'ellipse'])
    center = (random.randint(50, width-50), random.randint(50, height-50))
    if shape_type == 'circle':
        radius = random.randint(20, 50)
        color = (255, 255, 255)
        thickness = -1  # Filled shape
        cv2.circle(image, center, radius, color, thickness)
        area = np.pi * radius ** 2
    else:
        axes = (random.randint(20, 50), random.randint(20, 50))
        angle = random.randint(0, 360)
        color = (255, 255, 255)
        thickness = -1  # Filled shape
        cv2.ellipse(image, center, axes, angle, 0, 360, color, thickness)
        area = np.pi * axes[0] * axes[1]
    return area


# Generate a dataset of images and save them to the output directory
# Add a file with the areas of the shapes in each image
if __name__ == "__main__":
    # Get the arguments from the command line
    if len(sys.argv) != 4:
        print("Usage: build_dataset.py <size> <output_dir> <overwrite>")
        print("Example: build_dataset.py 1000 ../dataset false")
        sys.exit(1)

    size = int(sys.argv[1])
    output_dir = sys.argv[2]
    overwrite = sys.argv[3] == "true"
    areas_file = os.path.join(output_dir, f'areas.txt')

    # Create the output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # Remove existing files if overwrite is True
    if overwrite:
        for file_name in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file_name)
            os.remove(file_path)

    # Generate the dataset
    success = True
        
    for i in range(size): 
        img = np.zeros((500, 500, 3), dtype=np.uint8)
        num_shapes = random.randint(1, 5)
        areas = []
        file_path = os.path.join(output_dir, f'image_{i:03d}.png')
        for _ in range(num_shapes):
            areas.append(draw_random_shape(img))
        success = cv2.imwrite(file_path, img)
        if not success:
            break
        areas.sort()
        with open(areas_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(areas)    

    if not success:
        print(f"Failed to save dataset to {output_dir}")
    else:
        print(f"Dataset saved to {output_dir}")