import shutil


def update_wordpress(source, destination):
    shutil.copytree(source, destination, dirs_exist_ok=True)


def main():
    # source directory: 'home/jkuatack/public_html/departments/aawp
    input1 = input("Source directory: ")
    # destination directory can be all the wordpress folders
    input2 = input("Destination directory: ")
    update_wordpress(input1, input2)


main()
