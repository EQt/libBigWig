project(bigwig)
add_library(BigWig SHARED
    io.c
    bwValues.c
    bwRead.c
    bwStats.c
    bwWrite.c
)
