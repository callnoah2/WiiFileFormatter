import os
import argparse
import shutil
import py7zr

def clean_filename(filename):
    # Function to clean up the filename by removing content inside parentheses
    parts = filename.split('(')
    return parts[0].strip()

def unzip_and_rename(zip_file, new_id, destination_path="/Volumes/WII/wbfs", overwrite=False):
    try:
        # Extract all files to a temporary folder
        temp_folder = "/tmp/FileFormatterTemp"
        os.makedirs(temp_folder, exist_ok=True)

        with py7zr.SevenZipFile(zip_file, mode='r') as archive:
            archive.extractall(temp_folder)

        # Get the list of extracted items
        extracted_items = os.listdir(temp_folder)

        # Create a new folder based on the cleaned filename and the provided ID
        clean_filename_without_extension = os.path.splitext(clean_filename(os.path.basename(zip_file)))[0]
        new_folder_name = f"{clean_filename_without_extension} [{new_id}]"
        new_folder_path = os.path.join(destination_path, new_folder_name)
        os.makedirs(new_folder_path, exist_ok=True)

        # Move each item into the new folder without renaming contents
        for extracted_item in extracted_items:
            extracted_item_path = os.path.join(temp_folder, extracted_item)
            new_item_path = os.path.join(new_folder_path, extracted_item)

            # Check if the item already exists
            if not overwrite and os.path.exists(new_item_path):
                print(f"Skipping {extracted_item} as it already exists.")
            else:
                # Move the item to the destination folder
                shutil.move(extracted_item_path, new_item_path)

        # Cleanup: Remove the temporary folder
        shutil.rmtree(temp_folder)

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