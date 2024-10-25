import os
from datetime import datetime, timedelta

# Folder containing images for each type (assumes the same folder structure as in the original script)

base_folders = [
    "satellite_images_sea_2",
    "satellite_images_sea_all",
]

image_types = [
    "NightMicrophysicsRGB",
    "DayMicrophysicsRGB",
    "DayConvectiveStorm",
    "Visible",
    "Infrared",
    "ShortWaveInfrared",
    "Sandwich",
    "HeavyRainfallPotentialAreas",
    "TrueColorEnhanced",
]

# Function to parse the timestamp from the filename format [year]_[month]_[day]_[UTC image index].jpg
def extract_time_from_filename(filename):
    try:
        # Example filename: 2024_10_23_0930.jpg
        parts = filename.split("_")
        if len(parts) != 4:
            return None
        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
        time_str = parts[3].split(".")[0]
        hour, minute = int(time_str[:2]), int(time_str[2:])
        return datetime(year, month, day, hour, minute)
    except Exception as e:
        print(f"Error parsing filename {filename}: {e}")
        return None

# Function to scan for missing files in a given image type folder
def scan_for_missing_files(image_type, base_folder):
    folder_path = os.path.join(base_folder, image_type)
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return []

    # List all the filenames in the folder
    existing_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    # Filter out None values before sorting
    existing_times = sorted([t for t in (extract_time_from_filename(f) for f in existing_files) if t is not None])

    # If no valid files are found, return early
    if not existing_times:
        print(f"No valid images found in {folder_path} folder.\n")
        return []

    missing_files = []
    current_time = existing_times[0]
    end_time = existing_times[-1]

    # Iterate through the expected timestamps and check if files are missing
    while current_time <= end_time:
        expected_filename = f"{current_time.year}_{current_time.month:02d}_{current_time.day:02d}_{current_time.hour:02d}{current_time.minute:02d}.jpg"
        if expected_filename not in existing_files:
            missing_files.append(expected_filename)
        current_time += timedelta(minutes=10)

    return missing_files

# Main function to scan all image types and report missing files
def scan_all_image_types(base_folder):
    all_missing_files = {}

    for image_type in image_types:
        print(f"Scanning for missing files in {os.path.join(base_folder, image_type)}...")
        missing_files = scan_for_missing_files(image_type, base_folder)
        if missing_files:
            all_missing_files[image_type] = missing_files
        print()
    
    if all_missing_files:
        print("\nSummary of missing files:")
        for image_type, files in all_missing_files.items():
            print(f"{os.path.join(base_folder, image_type)}:")
            for file in files:
                print(f"  {file}")
            print()
    else:
        print("No missing files detected.")

# Run the scanning process
if __name__ == "__main__":
    for base_folder in base_folders:
        print('------------------------------------------')
        print('Base Folder :', base_folder)
        print('------------------------------------------')
        scan_all_image_types(base_folder)
        print()
