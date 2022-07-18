"""
This file is run after a successfull build of the frontend.

Moves files etc. to the correct directories and gzips js.
"""

import gzip
import os
import shutil
from distutils.dir_util import copy_tree

root_dir = os.path.abspath(os.path.dirname(__file__))
build_folder = os.path.join(root_dir, "flandria-frontend", "build")
templates_folder = os.path.join(root_dir, "webapp", "templates")
static_folder = os.path.join(root_dir, "webapp", "static")


def clean_than_copy_path(source_path, target_path):
    shutil.rmtree(target_path, ignore_errors=True)
    copy_tree(source_path, target_path)


# Create folders
if not os.path.exists(templates_folder):
    os.mkdir(templates_folder)
if not os.path.exists(static_folder):
    os.mkdir(static_folder)

# Copy relevant files from build to webapp folder
shutil.copyfile(os.path.join(build_folder, "index.html"), os.path.join(templates_folder, "index.html"))
shutil.copyfile(os.path.join(build_folder, "favicon.ico"), os.path.join(static_folder, "favicon.ico"))
clean_than_copy_path(os.path.join(build_folder, "assets"), os.path.join(static_folder, "assets"))
clean_than_copy_path(os.path.join(build_folder, "static", "files"), os.path.join(static_folder, "files"))
clean_than_copy_path(os.path.join(build_folder, "static", "css"), os.path.join(static_folder, "css"))

shutil.rmtree(os.path.join(static_folder, "js"), ignore_errors=True)
os.mkdir(os.path.join(static_folder, "js"))

# Only copy specific files from js-folder
for fname in os.listdir(os.path.join(build_folder, "static", "js")):
    if not (fname.endswith("js") or fname.endswith("map")):
        continue

    shutil.copy(os.path.join(build_folder, "static", "js", fname), os.path.join(static_folder, "js", fname))

    # Write original content to gzipped file
    with open(os.path.join(build_folder, "static", "js", fname), "rb") as fp:
        gzip.GzipFile(os.path.join(static_folder, "js", f"{fname}.gz"), "w").write(fp.read())
