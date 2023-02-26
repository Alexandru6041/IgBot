# IMPORTS
import os
import importlib.metadata
from importlib import reload
import pkg_resources
import subprocess

# VARIABLES
mainfolder = os.path.dirname(os.path.abspath(__file__))


def strstr(string1, string2):
    for i in range(min(len(string1), len(string2))):
        if (ord(string1[i]) < ord(string2[i])):
            return string1
        elif (ord(string1[i]) > ord(string2[i])):
            return string2

    if (len(string1) < len(string2)):
        return string1
    else:
        return string2


class Installer(object):
    def __init__(self, reqFile):
        self.reqFile = reqFile

    def __checkinstall(file: str):
        missing = True
        file = str(file).lower()
        installed = pkg_resources.working_set
        installed_list = sorted(i.key for i in installed)

        for i in range(len(installed_list)):
            if installed_list[i] == file:
                missing = False
                break

            if (strstr(file.lower(), installed_list[i]) == file):
                break

        if missing == True:
            subprocess.check_call(
                ['python', '-m', 'pip', 'install', file], stdout=subprocess.DEVNULL)
            installed = reload(pkg_resources)
            return Installer.__checkinstall(file)

        else:
            return True

    def __checklibrary(file: str, version):
        lib_validation = Installer.__checkinstall(file)

        if (lib_validation == True):
            lib_version = importlib.metadata.version(file)
            print(f"{file} installed. Version: {version}\n\n")

        if (lib_version != version):
            subprocess.check_call(
                ['python', '-m', 'pip', 'install', file, '--upgrade'], stdout=subprocess.DEVNULL)
            return Installer.__checklibrary(file, version)
        else:
            return True

    def checklibraries(self):
        with open(self.reqFile, "r") as f:
            content = f.readlines()

            for i in content:
                current_lib = i.strip()
                current_lib = current_lib.split("==")
                required_lib_name = current_lib[0]
                required_lib_version = current_lib[1]
                if (Installer.__checklibrary(required_lib_name, required_lib_version) == True):
                    pass

    def __run(self):
        Ist = Installer(self)
        Ist.checklibraries()

    def RunInstaller(self):
        return Installer.__run(self)
