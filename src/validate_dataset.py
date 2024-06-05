import os
import sys
import cv2
import csv
import matplotlib.pyplot as plt


def measure_shapes_area(image_path):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold the image to get binary image
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Calculate areas
    areas = [cv2.contourArea(contour) for contour in contours]
    
    return image, contours, areas


def draw_contours(image, contours, areas, file_path, save=False):
    # Draw contours on the image
    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    
    # Display the image with contours using matplotlib
    plt.figure(figsize=(5, 5))
    plt.title('Contours on Image')
    plt.axis('off')
    # Make figure fit the image
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    # Annotate the image with area sizes
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        plt.text(x, y - 10, f'Area: {areas[i]:.2f}', color='red', fontsize=12, backgroundcolor='white')
    
    # Save image to file
    if file_path:
        plt.savefig(file_path)
    else:
        plt.show()


# Read images from dataset, process images and save results to validation directory
# Compare training data with validation data
if __name__ == "__main__":
    # Get the arguments from the command line
    if len(sys.argv) != 3:
        print("Usage: validate_dataset.py <dataset_dir> <validation_dir>")
        print("Example: validate_dataset.py ../dataset ../validation")
        sys.exit(1)

    dataset_dir = sys.argv[1]
    validation_dir = sys.argv[2]
    areas_file = os.path.join(validation_dir, f'computed_areas.txt')

    # Create the output directory if it does not exist
    os.makedirs(validation_dir, exist_ok=True)
    for file_name in os.listdir(validation_dir):
        file_path = os.path.join(validation_dir, file_name)
        os.remove(file_path)

    size = len(os.listdir(dataset_dir))
    for i in range(size):
        
        # Process image and save results values
        image_path = os.path.join(dataset_dir, f'image_{i:03d}.png')
        if not os.path.isfile(image_path):
            continue
        image, contours, areas = measure_shapes_area(image_path)
        areas.sort()
        with open(areas_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(areas)    
        
        # Save image with contours
        result_path = os.path.join(validation_dir, f'result_{i:03d}.png')
        draw_contours(image, contours, areas, result_path)
        
        