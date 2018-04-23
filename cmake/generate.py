"""
Generate/update CMakeLists.txt by simulating make
"""
import subprocess as sp
import re
import os
import yaml
from six.moves.urllib import request



def raw_github(fname, owner="conda", repo="conda-recipes", branch="master"):
    return f"https://github.com/{owner}/{repo}/raw/{branch}/{fname}"


def zlib_extern(cm):
    url = raw_github("zlib/meta.yaml")
    meta = yaml.load(request.urlopen(url))
    print(f"externalproject_add({meta['package']['name']}", file=cm)
    print(f"    URL_MD5={meta['source']['md5']}", file=cm)
    print(f"    URL={meta['source']['url']}", file=cm)
    print(")", file=cm)


if __name__ == '__main__':
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))

    make = sp.run("make --always-make --dry-run libBigWig.so".split(),
                  stdout=sp.PIPE).stdout.decode().split('\n')
    assert len(make) > 1, make
    assert make.pop() == ''
    assert '-shared' in make[-1]
    sources = [s.split(' ')[-1] for s in make[:-1]]

    with open("CMakeLists.txt", "w") as cm:
        print("""cmake_minimum_required(VERSION 3.0)

project(bigwig)
set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")

find_package(LibZ)

include_directories(${ZLIB_INCLUDE_DIR})

add_library(BigWig SHARED""", file=cm)
        for s in sources:
            print("   ", s, file=cm)
        print(")", file=cm)
        print(file=cm)
        print("target_link_libraries(BigWig ${ZLIB_LIBRARY})", file=cm)
        print("if (TARGET zlib)", file=cm)
        print("    add_dependencies(BigWig zlib)", file=cm)
        print("endif()", file=cm)
        print("""
if (WIN32)
    add_definitions(-DNOCURL)
endif()""", file=cm)
        # zlib_extern(cm)
