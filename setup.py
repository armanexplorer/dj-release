########################################################
# This program builds .so files from .py files
# and delete '.py', '.c' and '.pyc' files.# install cpython:
# sudo pip install cython
# Command to run build:
# python compile.py build_ext --inplace
########################################################

import os
import sys
from distutils.core import setup
from distutils.extension import Extension
from pathlib import Path

from Cython.Build import cythonize

# Get current folder path
print("------------ COMPILING ------------\n", flush=True)
mash_path = os.environ.get('PROJECT_PATH') or os.path.dirname(sys.argv[0])
print(mash_path, flush=True)

### Get .py files
extensions = []
excludefiles = ['compile', '__init__', 'urls', 'manage', 'settings', 'credentials', 'apps']

### build .so files from .py files ###
for file in list(Path(mash_path).glob('**/*.py')):
    # Take out file name without .py ext
    filename = Path(file).resolve().stem
    # print(Path(file).resolve().parent)
    if file.stat().st_size != 0 and filename not in excludefiles and Path(file).resolve().parent.stem != 'migrations':
        package_name = file.relative_to(mash_path).parent / filename
        package_name = '.'.join(package_name.with_suffix('').parts)
        print(package_name)
        print(str(file))
        # print(package_name)
        # relpath = os.path.relpath(os.path.dirname(file.absolute().as_posix()), mash_path)
        # packagename = relpath.replace('/', '.') + '.' + filename if relpath != '.' else filename
        # print(packagename)
        extensions.append([Extension(package_name, [str(file)])])

for ext in extensions:
    setup(ext_modules=cythonize(ext, compiler_directives={
        'c_string_type': 'str',
        'c_string_encoding': 'utf8',
        'language_level': 3}),
        options={'build':{'build_lib':'.release'}}
          )

def deletefiles(file_type):
    cfiles = list(Path(mash_path).glob('**/*.' + file_type))
    for cfile in cfiles:
        filename = Path(cfile).resolve().stem
        if (filename not in excludefiles) and (cfile.resolve().parent.stem != 'migrations'):
            cfile.unlink()
            
def aux_delete_files():
    for f in list(Path(mash_path).glob('**/*.')):
        filename = Path(f).resolve().stem
        if (filename in ['.git', '.gitignore']):
            f.unlink()

### delete *.py files ###
deletefiles('py')

### delete *.c files #####
deletefiles('c')

### delete *.pyc files #####
deletefiles('pyc')

### delete unnecessary files ###
aux_delete_files()
