"""
Generate/update CMakeLists.txt by simulating make
"""
import subprocess as sp
import re
from six.moves.urllib import request
import yaml


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
    make = sp.run("make --always-make --dry-run libBigWig.so".split(),
                  stdout=sp.PIPE).stdout.decode().split('\n')
    assert make.pop() == ''
    assert '-shared' in make[-1]
    sources = [s.split(' ')[-1] for s in make[:-1]]


    with open("CMakeLists.txt", "w") as cm:
        print("project(bigwig)", file=cm)
        print(file=cm)
        print("add_library(BigWig SHARED", file=cm)
        for s in sources:
            print("   ", s, file=cm)
        print(")", file=cm)
        print(file=cm)
        zlib_extern(cm)
