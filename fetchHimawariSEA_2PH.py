import os
import requests
from datetime import datetime, timedelta, timezone

# Define base URLs for different types of imagery
urls = {
    "NightMicrophysicsRGB"       : "https://www.data.jma.go.jp/mscweb/data/himawari/img/se2/se2_ngt_",
    "DayMicrophysicsRGB"         : "https://www.data.jma.go.jp/mscweb/data/himawari/img/se2/se2_dms_",
    "DayConvectiveStorm"         : "https://www.data.jma.go.jp/mscweb/data/himawari/img/se2/se2_cve_",
    "Visible"                    : "https://www.data.jma.go.jp/mscweb/data/himawari/img/se2/se2_b03_",
    "Infrared"                   : "https://www.data.jma.go.jp/mscweb/data/himawari/img/se2/se2_b13_",
    "ShortWaveInfrared"          : "https://www.data.jma.go.jp/mscweb/data/himawari/img/se2/se2_b07_",
    "Sandwich"                   : "https://www.data.jma.go.jp/mscweb/data/himawari/img/se2/se2_snd_",
    "HeavyRainfallPotentialAreas": "https://www.data.jma.go.jp/mscweb/data/himawari/img/se2/se2_hrp_",
    "TrueColorEnhanced"          : "https://www.data.jma.go.jp/mscweb/data/himawari/img/se2/se2_trm_"
}

# Folder to save images
output_folder = "satellite_images_sea_2"
last_utc_file = "last_utc_time_sea_2.checkpoint"

# Create folders for each type of imagery if they don't exist
for image_type in urls.keys():
    folder_path = os.path.join(output_folder, image_type)
    os.makedirs(folder_path, exist_ok=True)

# Function to download an image based on the URL and save it
def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {save_path}")
        else:
            print(f"Failed to download {url}: Status {response.status_code}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Function to generate the image indices based on time range
def generate_image_indices(start_time, end_time):
    indices = []
    current_time = start_time
    while current_time <= end_time:
        index = f"{current_time.hour:02d}{(current_time.minute // 10) * 10:02d}"
        indices.append((index, current_time))
        current_time += timedelta(minutes=10)
    return indices

# Read the last recorded UTC time from file
def get_last_utc_time():
    if os.path.exists(last_utc_file):
        with open(last_utc_file, 'r') as f:
            last_time_str = f.read().strip()
            return datetime.strptime(last_time_str, '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
    return None

# Save the current UTC time to file
def save_current_utc_time(current_time):
    with open(last_utc_file, 'w') as f:
        f.write(current_time.strftime('%Y-%m-%d %H:%M'))

# Function to download images in a round-robin manner
def download_images_in_sequence(start_time, end_time):
    indices = generate_image_indices(start_time, end_time)
    
    # Loop through each time point and download one image from each type at that time
    for img_index, img_time in indices:
        for image_type, base_url in urls.items():
            url = f"{base_url}{img_index}.jpg"
            # Create filename in the format [year]_[month]_[day]_[UTC image index]
            filename = f"{img_time.year}_{img_time.month:02d}_{img_time.day:02d}_{img_index}.jpg"
            folder_path = os.path.join(output_folder, image_type)
            save_path = os.path.join(folder_path, filename)
            download_image(url, save_path)
        print("\n")

# Main function to determine the download range
def download_new_images():
    current_utc_time = datetime.now(timezone.utc)  # Use timezone-aware datetime in UTC
    # Subtract 30 minutes from current time to avoid incomplete or unavailable images
    current_utc_time -= timedelta(minutes=30)

    last_utc_time = get_last_utc_time()

    if last_utc_time:
        # Download images from last recorded time to current time
        start_time = last_utc_time
    else:
        # First run: download images from 23 hours ago to current time
        start_time = current_utc_time - timedelta(hours=23)

    # Download the images in sequence and update the last recorded UTC time
    download_images_in_sequence(start_time, current_utc_time)
    save_current_utc_time(current_utc_time)

# Run the download process
if __name__ == "__main__":
    download_new_images()
