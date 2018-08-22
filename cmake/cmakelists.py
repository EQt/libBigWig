#!/usr/bin/env python
"""
Generate/update CMakeLists.txt by simulating make
"""
import subprocess as sp
import yaml
import re
from os import path
from six.moves.urllib import request


header = """cmake_minimum_required(VERSION 3.0)

project(bigwig)
set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")

find_package(LibZ)
find_package(CURL)

include_directories(${ZLIB_INCLUDE_DIR})
"""

footer = """
if (CURL_FOUND)
    include_directories(${CURL_INCLUDE_DIRS})
    target_link_libraries(BigWig ${CURL_LIBRARIES})
else()
    add_definitions(-DNOCURL)
endif()"""


def raw_github(fname, owner="conda", repo="conda-recipes", branch="master"):
    return f"https://github.com/{owner}/{repo}/raw/{branch}/{fname}"


def zlib_extern(cm):
    url = raw_github("zlib/meta.yaml")
    meta = yaml.load(request.urlopen(url))
    print(f"externalproject_add({meta['package']['name']}", file=cm)
    print(f"    URL_MD5={meta['source']['md5']}", file=cm)
    print(f"    URL={meta['source']['url']}", file=cm)
    print(")", file=cm)


def emulate_make(target='libBigWig.so', cwd=None):
    cmd = "make --always-make --dry-run " + target
    return sp.run(cmd.split(), stdout=sp.PIPE, cwd=cwd).stdout.decode().split('\n')


def generate_cmakelists(root):
    make = emulate_make('libBigWig.so', cwd=root)
    assert len(make) > 1, make
    assert make.pop() == ''
    assert '-shared' in make[-1]
    sources = [s.split(' ')[-1] for s in make[:-1]]

    tests = emulate_make('test', cwd=root)
    tests = [t for t in tests if '-o test/' in t]
    static_tests = [t for t in tests if 'libBigWig.a' in t]

    def print_tests(cm):
        print('include_directories(".")', file=cm)
        print(file=cm)
        for t in static_tests:
            [name] = re.findall(r'-o test/(\w+)', t)
            sources = ' '.join(re.findall(r'(test/\w+\.c)', t))
            print(f"add_executable({name} {sources})", file=cm)
            print(f"target_link_libraries({name} BigWigS)", file=cm)

    with open(path.join(root, "CMakeLists.txt"), "w") as cm:
        print(header, file=cm)
        print("add_library(BigWig SHARED", file=cm)
        for s in sources:
            print("   ", s, file=cm)
        print(")", file=cm)
        print(file=cm)
        print("target_link_libraries(BigWig ${ZLIB_LIBRARY})", file=cm)
        print("if (TARGET zlib)", file=cm)
        print("    add_dependencies(BigWig zlib)", file=cm)
        print("endif()", file=cm)
        print(file=cm)

        print("add_library(BigWigS STATIC", file=cm)
        for s in sources:
            print("  ", s, file=cm)
        print(")", file=cm)
        print(file=cm)

        print_tests(cm)

        print(footer, file=cm)


if __name__ == '__main__':
    root = path.join(path.dirname(__file__), '..')
    generate_cmakelists(root=root)
    # zlib_extern(cm)
