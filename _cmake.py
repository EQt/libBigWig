"""
Generate/update CMakeLists.txt by simulating make
"""
import subprocess as sp
import re

make = sp.run("make --always-make --dry-run libBigWig.so".split(),
              stdout=sp.PIPE).stdout.decode().split('\n')
assert make.pop() == ''
assert '-shared' in make[-1]
sources = [s.split(' ')[-1] for s in make[:-1]]


with open("CMakeLists.txt", "w") as cm:
    print("project(bigwig)", file=cm)
    print("add_library(BigWig SHARED", file=cm)
    for s in sources:
        print("   ", s, file=cm)
    print(")", file=cm)
