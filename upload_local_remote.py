from ftplib import FTP
import os


def main():
    local_directory = input("Enter local directory: ")
    remote_directory = input("Enter remote directory: /")
    update_from_folder(local_directory, remote_directory, get_ftp())


def get_ftp():
    ftp = FTP("jkuat.ac.ke")
    ftp.login("jkuatack", "0=:!%q.0(pX")
    ftp.cwd("public_html/departments/aawp")
    ftp.retrlines("LIST")
    return ftp


def update_from_folder(pathname, working_dir, ftp):
    folder = os.listdir(pathname)
    for i in folder:
        new_local_name = os.path.join(pathname, i)
        if os.path.isdir(new_local_name):
            new_working_dir = working_dir + f"/{i}"
            ftp.cwd(f"/{new_working_dir}")
            print(f"Changed to folder: {new_local_name}")
            update_from_folder(new_local_name, new_working_dir, ftp)
        else:
            upload_ftp_file(ftp, i, new_local_name)


def upload_ftp_file(ftp, filename, pathname):
    transfer_file = open(pathname, "rb")
    ftp.storbinary(f"STOR {filename}", transfer_file)
    print(f"Saved file: {filename}")


main()
