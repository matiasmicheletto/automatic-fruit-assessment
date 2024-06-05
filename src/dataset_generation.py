import cv2
import numpy as np
import os
import random

# Create a directory to save generated images
os.makedirs('generated_images', exist_ok=True)

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
    else:
        axes = (random.randint(20, 50), random.randint(20, 50))
        angle = random.randint(0, 360)
        color = (255, 255, 255)
        thickness = -1  # Filled shape
        cv2.ellipse(image, center, axes, angle, 0, 360, color, thickness)

# Generate 100 images
for i in range(100):
    img = np.zeros((500, 500, 3), dtype=np.uint8)
    num_shapes = random.randint(1, 5)
    for _ in range(num_shapes):
        draw_random_shape(img)
    cv2.imwrite(f'generated_images/image_{i+1:03d}.png', img)

print("100 images with random shapes generated and saved.")
