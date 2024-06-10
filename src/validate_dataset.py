import os
import sys
import csv


# Compare training data with validation data
if __name__ == "__main__":
    # Get the arguments from the command line
    if len(sys.argv) != 3:
        print("Usage: validate_dataset.py <dataset_dir> <validation_dir>")
        print("Example: validate_dataset.py ../dataset ../validation")
        sys.exit(1)

    dataset_dir = sys.argv[1]
    validation_dir = sys.argv[2]
    
    areas_file = os.path.join(dataset_dir, f'areas.txt')
    computed_areas_file = os.path.join(validation_dir, f'computed_areas.txt')

    with open(areas_file, 'r') as f:
        reader = csv.reader(f)
        dataset_areas = [list(map(float, row)) for row in reader]
        with open(computed_areas_file, 'r') as f:
            reader = csv.reader(f)
            validation_areas = [list(map(float, row)) for row in reader]
            
            detected_mismatch = 0
            errors = []
            for dataset, validation in zip(dataset_areas, validation_areas):
                if len(dataset) != len(validation):
                    detected_mismatch += 1
                else:
                    diff = [abs(d - v) for d, v in zip(dataset, validation)]
                    error = sum(diff) / len(dataset)
                    errors.append(error)

            avg_error = sum(errors) / len(errors)
            std_dev = (sum([(error - avg_error) ** 2 for error in errors]) / len(errors)) ** 0.5

            print(f'Detected mismatch: {detected_mismatch} out of {len(dataset_areas)} images')
            #print(f'Average error: {avg_error}')
            print(f'Relative error: {avg_error / sum(errors)}')
            print(f'Standard deviation: {std_dev}')