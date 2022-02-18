from ftplib import FTP


def get_ftp():
    ftp = FTP("jkuat.ac.ke")
    ftp.login("jkuatack", "0=:!%q.0(pX")
    ftp.cwd("public_html/python_scripts")
    ftp.retrlines("LIST")
    return ftp


def upload_file(file_path, file_name):
    ftp = get_ftp()
    file = open(file_path, "rb")
    cmd = "STOR " + file_name
    ftp.storbinary(cmd, file)


def main():
    file_path = input("Enter file path: ")
    file_name = input("Enter file name: ")
    upload_file(file_path, file_name)


main()
