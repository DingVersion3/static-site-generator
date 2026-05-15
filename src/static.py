import os
import shutil

def copy_static(src, dst):
    # The "Commander" step: clean the whole 'docs' folder once
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    # Start the recursive process
    copy_recursive(src, dst)

def copy_recursive(src, dst):
    for item in os.listdir(src):
        # Ignore Windows metadata and Mac system files
        if item.endswith(".Identifier") or item == ".DS_Store":
            continue

        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            print(f"copying {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            # Create the sub-folder and recurse into it
            os.mkdir(dst_path)
            copy_recursive(src_path, dst_path)