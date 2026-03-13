#Computer\HKEY_LOCAL_MACHINE\SOFTWARE\\WOW6432Node\\Sims\\The Sims 3

import winreg
from glob import iglob
import os


class DiscInstall:
    def __init__(self):
        self.install_directory = None

    def find_install_directory(self, pack_key):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\Sims\\{}".format(pack_key))
            self.install_directory = winreg.QueryValueEx(key, "Install Dir")[0]
        except:
            return False
        return True
    def get_all_files_matching_pattern(self, pattern):
        formatted_pattern = self.install_directory + os.sep + pattern
        #print(pattern, formatted_pattern)

        return list(iglob(formatted_pattern, recursive=True))

    def get_builds(self, prefix):
        return self.get_all_files_matching_pattern("**{}{}{}.{}".format(os.sep, prefix, "*", "package"))

    def get_fullbuilds(self):
        return self.get_builds("Full")

    def get_deltabuilds(self):
        return self.get_builds("Delta")

    def get_convertable_files(self):
        return [*self.get_fullbuilds(), *self.get_deltabuilds()]


