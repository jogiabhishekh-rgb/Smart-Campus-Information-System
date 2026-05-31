import os

class MissingFileOrFolderError(Exception):
    pass

def scan_directory(path):
    try:
        if not os.path.exists(path):
            raise FileNotFoundError("Invalid Directory")

        for root, dirs, files in os.walk(path):
            level = root.replace(path, "").count(os.sep)
            indent = " " * 4 * level

            print(f"{indent}{os.path.basename(root)}/")

            for file in files:
                print(" " * 4 * (level + 1) + file)

            if not files and not dirs:
                raise MissingFileOrFolderError(
                    f"Empty Folder Detected: {root}"
                )

    except FileNotFoundError as e:
        print(e)

    except MissingFileOrFolderError as e:
        print(e)

path = input("Enter directory path: ")
scan_directory(path)
