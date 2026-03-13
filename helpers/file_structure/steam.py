from helpers.file_structure.disc import DiscInstall
import winreg

class SteamInstall(DiscInstall):
    def find_install_directory(self, pack_key):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\Sims\\{}".format(pack_key))
            self.install_directory = winreg.QueryValueEx(key, "Install Dir")[0]
        except:
            return False
        return True