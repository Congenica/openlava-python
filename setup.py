# Copyright 2013 David Irvine
#
# This file is part of openlava-python
#
# openlava-python is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# openlava-python is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with openlava-python.  If not, see <http://www.gnu.org/licenses/>.

#this only works with --inplace for now? no idea why
#python setup.py build_ext --inplace

import os, os.path
import glob
#from distutils.core import setup
from setuptools import setup
from distutils.extension import Extension
from Cython.Build import cythonize

#openlava.utils has a find_openlava method that we need here,
#but we can't import it yet because we haven't installed the module
with open('openlava/utils.py') as f: 
    exec(f.read())

lsf_dir = find_openlava()
print "Detected openlava dir: {}".format(lsf_dir)

inc_dir = os.path.join(lsf_dir, "include")
lib_dir = os.path.join(lsf_dir, "lib")

#without these lserrno can't be found, i don't know why.
#need to fix that really
lsf = os.path.join(lsf_dir, "lib", "liblsf.a")
lsbatch = os.path.join(lsf_dir, "lib", "liblsbatch.a")

if not os.path.exists(lsf):
    raise ValueError("Cannot find liblsf.a ({} does not exist)".format(lsf))
if not os.path.exists(lsbatch):
    raise ValueError("Cannot find lsbatch.a ({} does not exist)".format(lsbatch))

extensions = [
    Extension(
        "*", ["openlava/*.pyx"],
        extra_compile_args = ["-O3", "-Wall"],
#        extra_link_args    = ['-rdynamic'], #something will need to be set here to get rid of the .a dependency
        runtime_library_dirs = [lib_dir], #so we don't need LD_LIBRARY_PATH
        extra_objects      = [lsf, lsbatch],
        libraries          = ['lsf','lsbatch','nsl'],
        include_dirs       = [inc_dir, "."],
        library_dirs       = [lib_dir],
    )
]

setup(
    name         = "openlava-bindings",
    version      = "1.2a",
    description  = "Bindings for OpenLava",
    author       = "David Irvine",
    author_email = "irvined@gmail.com",
    url          = "https://github.com/congenica/openlava-python",
    license      = "GPL 3",
    ext_modules  = cythonize(extensions),
    test_suite   = 'tests.test.suite',
    packages     = ['openlava'],
    classifiers  = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Topic :: Scientific/Engineering',
    ],
)
