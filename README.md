# Wii File Formatter

## Overview

The Wii File Formatter is a Python script designed to unzip files, remove content inside parentheses from the file name, and organize the extracted files into a new folder with a specified ID.

## Requirements

- Python 3.x
- py7zr library (install using `pip install py7zr`)
- tqdm library (install using `pip install tqdm`)

## Usage

1. Clone or download the repository to your local machine.

```bash
git clone https://github.com/callnoah2/WiiFileFormatter
```
Navigate to the file directory
```bash
cd wii-file-formatter
```
Run the script with the following command:
```bash
python FileFormatter.py <path/to/your/file.7z> <new_id> [<optional/destinaiton>] [--overwrite]

### Arguments

- <path/to/your/file.7z>: Path to the zipped file you want to extract and organize.
- [<destination_path>] (optional): Destination path for extracted files (default: "/Volumes/WII/wbfs").
- [--overwrite] (optional): Include this flag to overwrite existing files in the destination folder.

