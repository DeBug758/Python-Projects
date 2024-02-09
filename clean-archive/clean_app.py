import argparse
import os
import shutil
import tempfile
import zipfile
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def unzip_archive(archive, res_dir):
    with zipfile.ZipFile(archive, 'r') as zf:
        zf.extractall(path=res_dir)
    logging.info("Archive unzipped successfully.")


def create_new_archive(archive, location):
    shutil.make_archive(location, 'zip', archive)
    logging.info(f"New archive created at: {location}")


def remove_folders_without_init(path):
    deleted = []
    for dirpath, dirnames, files in os.walk(path):
        if dirpath != path and '__init__.py' not in files:
            path_parts = dirpath.split('/')
            if path_parts[0] == '':
                trimmed_path_parts = path_parts[3:]
            else:
                trimmed_path_parts = path_parts[2:]
            trimmed_path = '/' + '/'.join(trimmed_path_parts)
            deleted.append(trimmed_path)
            shutil.rmtree(dirpath)
    deleted.sort()
    with open(path + '/cleaned.txt', 'w') as file:
        for line in deleted:
            file.write(line[1:] + '\n')


def main():
    parser = argparse.ArgumentParser(description="Process a zip file.")
    parser.add_argument('archive_path', type=str, help='Path to the zip file to process')
    args = parser.parse_args()

    #cleaned_path = os.path.join(os.path.dirname(args.archive_path), 'cleaned.txt')
    #with open(cleaned_path, 'w') as file:
    #    pass
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        unzip_archive(args.archive_path, temp_dir)

        remove_folders_without_init(temp_dir)
        res = args.archive_path.split('.')[0] + '_new'
        create_new_archive(temp_dir, res)


if __name__ == "__main__":
    main()
