import os
import shutil

source = "/home/raphael/Downloads/aawp"


def update_wordpress(source, destination):
    shutil.copytree(source, destination, dirs_exist_ok=True)


def main():
    directory = input("Enter filepath: ")
    dig_directory(directory)


def dig_directory(pathname):
    folder = os.listdir(pathname)
    if "wp-admin" and "wp-content" and "wp-includes" in folder:
        print(f"{pathname} This is a wordpress folder!")
        update_wordpress(source, pathname)
    for i in folder:
        new_path_name = os.path.join(pathname, i)
        if os.path.isdir(new_path_name):
            dig_directory(new_path_name)


main()
