
#Relative path to the folder containing all files:
input_folder = r"FolderWithAllPhotos" # Path to the folder containing all files
output_folder = r"SortedFiles" # Path to the folder where sorted files will be saved

import os
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

# Change relative path to absolute path if needed
if not os.path.isabs(input_folder):
    input_folder = os.path.abspath(input_folder)
if not os.path.isabs(output_folder):
    output_folder = os.path.abspath(output_folder)

print("Input folder: " + input_folder)
print("Output folder: " + output_folder)

# Get the creation date of jpg photo in the input folder
def get_creation_date(file_path):
    # Get the origin date taken of the photo file with PIL library in format YYYY-MM-DD
    try:
        img = Image.open(file_path)
        exif_data = img._getexif()
        if exif_data is not None:
            for tag, value in exif_data.items():
                if TAGS.get(tag) == 'DateTimeOriginal':
                    return value.split(' ')[0].replace(':', '-')
    except Exception as e:
        print(f"Error getting creation date for {file_path}: {e}")


#Main function to sort files
print("Sorting files...")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all files in the input folder
for filename in os.listdir(input_folder):
    # Get the full path of the file
    file_path = os.path.join(input_folder, filename)
    # Check if the file is a jpg photo
    if filename.lower().endswith('.jpg'):
        # Get the creation date of the file
        creation_date = get_creation_date(file_path)
        # Create a new folder for the creation date if it doesn't exist
        date_folder = os.path.join(output_folder, creation_date)
        if not os.path.exists(date_folder):
            os.makedirs(date_folder)
        # Copy the file to the new folder with the creation date
        new_file_path = os.path.join(date_folder, filename)
        shutil.copy2(file_path, new_file_path)
        # Uncomment the next line to move instead of copy
        #os.rename(file_path, new_file_path)
        print(f"Copy {filename} to {date_folder}")
    else:
        # If the file is not a jpg photo, move it to the "Other" folder
        other_folder = os.path.join(output_folder, "Other")
        if not os.path.exists(other_folder):
            os.makedirs(other_folder)
        new_file_path = os.path.join(other_folder, filename)
        shutil.copy2(file_path, new_file_path)
        # Uncomment the next line to move instead of copy
        #os.rename(file_path, new_file_path)
        print(f"Copy {filename} to {other_folder}")
print("Sorting completed.")
#End of code
