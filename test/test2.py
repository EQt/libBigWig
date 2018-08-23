#!/usr/bin/env python
"""
Rewrite test.py to be more portable:
 * not depend on md5 or md5sum executable
 * support Python3
"""
import hashlib
import subprocess as sp
from os import path
from os import remove


cwd = path.dirname(path.realpath(__file__))     # directory of this script


def check_md5(md5, msg, cmd, check='-'):
    print(msg.ljust(50), end='', flush=True)
    r = sp.check_output(cmd.split(), cwd=cwd)
    d = None
    if check == '-':
        d = hashlib.md5(r).hexdigest()
    elif path.exists(check):
        d = hashlib.md5(open(check, "rb").read()).hexdigest()
        remove(check)
    else:
        raise RuntimeError("Don't understand check = " + check)
    if d == md5:
        print('[OK]')
    else:
        assert False, str(d) + " != " + str(md5)


if __name__ == '__main__':
    check_md5("1c52065211fdc44eea45751a9cbfffe0", "local test",
              "./testLocal test.bw")
    check_md5("9ccecd6c32ff31042714c1da3c0d0eba", "remote http test",
              "./testRemote http://hgdownload.cse.ucsc.edu/goldenPath/hg19/" +
              "encodeDCC/wgEncodeMapability/wgEncodeCrgMapabilityAlign50mer.bigWig")
    check_md5("8e116bd114ffd2eb625011d451329c03", "test recreating a file",
              "./testWrite test.bw output.bw", "output.bw")
    check_md5("ef104f198c6ce8310acc149d0377fc16",
              "test creation from scratch with multiple interval types",
              "./exampleWrite", check="example_output.bw")