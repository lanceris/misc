import os


def collect_files(path, mode='an', ext=None):
    extensions = {}
    if mode == 'n':
        """Scans <path> directory for *.<ext>, without subdirectories"""
        if ext:
            for paths, subdirs, files in os.walk(path):
                for each in files:
                    if os.path.splitext(each)[-1] == '.{}'.format(ext):
                        x = os.path.splitext(each)[1]
                        if x not in extensions:
                            extensions[x] = []
                            extensions[x].append(os.path.join(paths, each))
                        else:
                            extensions[x].append(os.path.join(paths, each))
                break

    elif mode == 'r':
        """Scans <path> directory for *.<ext> recursively"""
        if ext:
            for paths, subdirs, files in os.walk(path):
                for each in files:
                    if os.path.splitext(each)[-1] == '.{}'.format(ext):
                        x = os.path.splitext(each)[1]
                        if x not in extensions:
                            extensions[x] = []
                            extensions[x].append(os.path.join(paths, each))
                        else:
                            extensions[x].append(os.path.join(paths, each))

    elif mode == 'an':
        """Scans <path> directory for all files, without subdirectories"""
        for paths, subdirs, files in os.walk(path):
            for each in files:
                x = os.path.splitext(each)[1]
                if x not in extensions:
                    extensions[x] = []
                    extensions[x].append(os.path.join(paths, each))
                else:
                    extensions[x].append(os.path.join(paths, each))
            break

    elif mode == 'ar':
        """Scans <path> directory for all files recursively"""
        for paths, subdirs, files in os.walk(path):
            for each in files:
                x = os.path.splitext(each)[1]
                if x not in extensions:
                    extensions[x] = []
                    extensions[x].append(os.path.join(paths, each))
                else:
                    extensions[x].append(os.path.join(paths, each))

    return extensions


def delete_empty_dirs(path):
    """Deletes empty dirs and subdirs in <path>"""
    c = 0
    for i in range(10):
        for paths, subdirs, files in os.walk(path):
            if len(os.listdir(paths)) == 0:
                os.rmdir(paths)
                c += 1
    return "Deleted {} directories".format(c)


def dump_files(path):
    """Collects files from all subdirectories and dumps them into <path>"""
    c = 0
    if type(path) == str:
        for paths, subdirs, files in os.walk(path):
            if paths != path:
                for file in files:
                    print(file)
                    # old_name = os.path.join(paths, file)
                    # new_name = os.path.join(path, file)
                    # try:
                    #     os.rename(old_name, new_name)
                    # except FileExistsError:
                    #     pass
    elif type(path) == dict:
        for each in path.values():
            for i in each:
                pass


def sort_files(ext_dict):
    #FIXME
    """Takes ext_dict from collect_files(),
     creates directory for each extension
     and moves files with that extension into directory."""
    for key, values in ext_dict.items():
        r = os.path.join(PATH, key[1:])
        os.mkdir(r)
        for item in values:
            os.rename(item, os.path.join(r, item.split('\\')[-1]))




PATH = r'C:\Users\lanceris\Desktop\testdir'
