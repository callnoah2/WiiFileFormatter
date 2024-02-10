import os
import zipfile
import argparse
from tqdm import tqdm
import shutil

def unzip_and_rename(zip_file, new_id, destination_path="/Volumes/WII/wbfs", overwrite=False):
    try:
        # Unzip the files
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # Use tqdm to display a progress bar
            extracted_files = tqdm(zip_ref.namelist(), desc="Extracting", unit="file")

            for file_name in extracted_files:
                extracted_files.set_postfix(file=file_name)
                zip_ref.extract(file_name, destination_path)

        # Get the list of extracted files
        extracted_files = os.listdir(destination_path)

        # Rename each file
        for file_name in extracted_files:
            old_path = os.path.join(destination_path, file_name)

            # Remove (USA) and (<languages>) and add [ID]
            new_name = file_name.replace('(USA)', '').replace('(<languages>)', '').strip() + f" [{new_id}]"

            # Construct the new path
            new_path = os.path.join(destination_path, new_name)

            # Check if the file already exists
            if not overwrite and os.path.exists(new_path):
                print(f"Skipping {new_name} as it already exists.")
            else:
                os.rename(old_path, new_path)
                print(f"Renamed {file_name} to {new_name}")

        print("Unzipping and renaming completed successfully.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unzip files and rename them.")
    parser.add_argument("zip_file", help="Path to the zipped file")
    parser.add_argument("new_id", help="New ID to be added in the filename")
    parser.add_argument("destination_path", nargs='?', default="/Volumes/WII/wbfs",
                        help="Destination path for extracted files (default: /Volumes/WII/wbfs)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")

    args = parser.parse_args()

    # Check if the required arguments are provided
    if not (args.zip_file and args.new_id):
        parser.print_usage()
        print("Error: Both 'zip_file' and 'new_id' are required.")
    else:
        unzip_and_rename(args.zip_file, args.new_id, args.destination_path, args.overwrite)