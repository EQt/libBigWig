project(bigwig)

add_library(BigWig SHARED
    io.c
    bwValues.c
    bwRead.c
    bwStats.c
    bwWrite.c
)

externalproject_add(zlib
    URL_MD5=44d667c142d7cda120332623eab69f40
    URL=http://zlib.net/zlib-1.2.8.tar.gz
)
