import os
import argparse
import shutil
import py7zr

def clean_filename(filename):
    # Function to clean up the filename by removing content inside parentheses
    parts = filename.split('(')
    return parts[0].strip()

def rename_wbfs_files(temp_folder, new_id):
    # Get a list of files in the specified path
    files = [f for f in os.listdir(temp_folder) if os.path.isfile(os.path.join(temp_folder, f))]

    # Iterate through each file
    for file_name in files:
        file_path = os.path.join(temp_folder, file_name)

        # Check if the file is a .wbfs file
        if file_name.endswith('.wbfs'):
            # Create the new file name with the provided ID
            new_file_name = f'{new_id}.wbfs'

            # Construct the new file path
            new_file_path = os.path.join(temp_folder, new_file_name)

            # Rename the file
            os.rename(file_path, new_file_path)
            print(f'Renamed: {file_name} to {new_file_name}')

def unzip_and_rename(zip_file, new_id, destination_path= "/Volumes/WII/wbfs", overwrite=False):
    new_id = new_id.upper()
    try:
        # Extract all files to a temporary folder
        temp_folder = "/tmp/FileFormatterTemp/" + new_id
        print(f"Making temp file called {temp_folder}")
        os.makedirs(temp_folder, exist_ok=True)

        with py7zr.SevenZipFile(zip_file, mode='r') as archive:
            archive.extractall(temp_folder)

        # Rename .wbfs files in the temporary folder
        rename_wbfs_files(temp_folder, new_id)

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
                try:
                    # Copy the item to the destination folder
                    shutil.copy2(extracted_item_path, new_item_path)

                    # Remove the original file after copying
                    os.remove(extracted_item_path)

                except Exception as move_error:
                    print(f"Error moving {extracted_item}: {move_error}")

        # Cleanup: Remove the temporary folder
        shutil.rmtree(temp_folder)

        print(f"\nUnzipping and renaming completed successfully for {new_folder_name}.\n")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    default_path = "/Volumes/WII/wbfs"
    parser = argparse.ArgumentParser(description="Unzip files and rename them.")
    parser.add_argument("zip_file", help="Path to the zipped file")
    parser.add_argument("new_id", help="New ID to be added in the filename")
    parser.add_argument("destination_path", nargs='?', default="default_path",
                        help="Destination path for extracted files (default: default_path)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")

    args = parser.parse_args()

    # Check if the required arguments are provided
    if not (args.zip_file and args.new_id):
        parser.print_usage()
        print("Error: Both 'zip_file' and 'new_id' are required.")
    elif len(args.new_id) != 6:
        raise ValueError("Error: New ID must be exactly 6 characters long.")
    else:
        unzip_and_rename(args.zip_file, args.new_id, args.destination_path, args.overwrite)