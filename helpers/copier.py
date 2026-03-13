import shutil
class Copier:
    def __init__(self, src_file, dst_folder):
        shutil.copy2(src_file, dst_folder)
