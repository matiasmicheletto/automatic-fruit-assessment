import cv2

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
    
    return areas

# Example usage
image_path = 'generated_images/image_001.png'
areas = measure_shapes_area(image_path)
print(f"Areas of shapes in {image_path}: {areas}")
