import hashlib
import os.path
from pathlib import Path
import re

SRC_FILES_PATH = Path("src_files.txt")

def run() -> None:

    # read list of source directories from file
    src_dirs = []
    with SRC_FILES_PATH.open('r', encoding="utf-8") as infile:
        for src in infile.readlines():
            src = src.strip()
            if os.path.exists(src): src_dirs.append(src)

    print(f"{len(src_dirs)} source files detected.")


    for src_dir in src_dirs:
        src_dir = Path(src_dir)
        
        hash_dict = dict()
        dup_list = []

        # Iterate through each source directory
        for src_file in src_dir.iterdir():
            if src_file.is_dir(): continue # Skip non-files

            # Create a hash string from the file contents
            with src_file.open('rb') as file_contents:
                hash_str = hashlib.md5(file_contents.read()).hexdigest()

            # check hash against existing hash strings
            if hash_str in hash_dict:
                # append original and duplicate files as a tuple
                dup_list.append((hash_dict[hash_str], str(src_file.resolve())))
            else:
                # add new hash string to dict
                hash_dict[hash_str] = str(src_file.resolve())

        if len(dup_list):
            print(f"<{src_dir}> contains {len(dup_list)} duplicates.")
            for dup in dup_list:
                print(dup,)
                # new_filename = re.sub(" \(\d\)", "", os.path.basename(dup[0]))
                # print(new_filename)
            print()

    pass

if __name__ == '__main__':
    # Create SRC_FILES_PATH if not exists
    if not SRC_FILES_PATH.exists():
        with SRC_FILES_PATH.open('w+') as _:
            pass

    run()