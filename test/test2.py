#!/usr/bin/env python
"""
Rewrite test.py to be more portable:
 * not depend on md5 or md5sum executable
 * support Python3
"""
import hashlib
import subprocess as sp
from os import path


cwd = path.dirname(path.realpath(__file__))     # directory of this script


def check_md5(md5, msg, cmd):
    print(msg.ljust(50), end='', flush=True)
    r = sp.check_output(cmd.split(), cwd=cwd)
    d = hashlib.md5(r).hexdigest()
    assert d == md5
    print('[OK]')


if __name__ == '__main__':
    check_md5("1c52065211fdc44eea45751a9cbfffe0", "local test",
              "./testLocal test.bw",)
    check_md5("9ccecd6c32ff31042714c1da3c0d0eba", "remote http test",
              "./testRemote http://hgdownload.cse.ucsc.edu/goldenPath/hg19/" +
              "encodeDCC/wgEncodeMapability/wgEncodeCrgMapabilityAlign50mer.bigWig")
