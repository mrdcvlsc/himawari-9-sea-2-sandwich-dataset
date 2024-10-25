import os

# Define the folder paths
folders = [
    "run_logs/fetchHimawariSEA_2PH",
    "run_logs/fetchHimawariSEA_ALL"
]

# Create each folder if it doesn't exist
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"Ensured folder exists: {folder}")
