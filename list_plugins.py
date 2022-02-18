import os
import logging


def list_plugins(site_url):
    # pathname = site_url.replace("https://www.jkuat.ac.ke/", "home/jkuatack/public_html")
    pathname = site_url
    plugin_dir = os.path.join(pathname, "wp-content/plugins")
    try:
        folder = os.listdir(plugin_dir)
        plugins = []
        for i in folder:
            plugin_name = os.path.join(plugin_dir, i)
            if os.path.isdir(plugin_name):
                plugins.append(i)
        print("Number of plugins :", len(plugins), "and they are:")
        print_list(plugins)

    except OSError as err:
        print("No such folder exists: ", err)


def dig_directory(pathname):
    folder = os.listdir(pathname)
    if "wp-admin" and "wp-content" and "wp-includes" in folder:
        foldername = pathname.replace("/home/jkuatack/public_html", "")
        print("--------------------", foldername, "--------------------")
        list_plugins(pathname)
    for i in folder:
        new_path_name = os.path.join(pathname, i)
        if os.path.isdir(new_path_name):
            dig_directory(new_path_name)


def main():
    pathname = "/home/jkuatack/public_html/departments"
    dig_directory(pathname)


def print_list(list):
    for i in list:
        print(i)


main()
