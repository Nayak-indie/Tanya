import os

def print_tree(start_path, prefix=""):
    try:
        entries = sorted(os.listdir(start_path))
    except PermissionError:
        print(prefix + "└── [Permission Denied]")
        return

    entries_count = len(entries)

    for index, entry in enumerate(entries):
        path = os.path.join(start_path, entry)
        is_last = index == entries_count - 1

        connector = "└── " if is_last else "├── "
        print(prefix + connector + entry)

        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            print_tree(path, prefix + extension)


if __name__ == "__main__":
    root_directory = os.getcwd()  # Change this if needed
    print(f"\nDirectory structure of: {root_directory}\n")
    print_tree(root_directory)
