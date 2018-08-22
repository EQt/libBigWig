cmake_minimum_required(VERSION 3.0)

project(bigwig)
set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")

find_package(LibZ)
find_package(CURL)

include_directories(${ZLIB_INCLUDE_DIR})

add_library(BigWig SHARED
    io.c
    bwValues.c
    bwRead.c
    bwStats.c
    bwWrite.c
)

target_link_libraries(BigWig ${ZLIB_LIBRARY})
if (TARGET zlib)
    add_dependencies(BigWig zlib)
endif()

add_library(BigWigS STATIC
   io.c
   bwValues.c
   bwRead.c
   bwStats.c
   bwWrite.c
)

include_directories(".")

add_executable(testLocal test/testLocal.c)
target_link_libraries(testLocal BigWigS)
add_executable(testRemote test/testRemote.c)
target_link_libraries(testRemote BigWigS)
add_executable(testWrite test/testWrite.c)
target_link_libraries(testWrite BigWigS)
add_executable(testRemoteManyContigs test/testRemoteManyContigs.c)
target_link_libraries(testRemoteManyContigs BigWigS)
add_executable(testBigBed test/testBigBed.c)
target_link_libraries(testBigBed BigWigS)
add_executable(testIterator test/testIterator.c)
target_link_libraries(testIterator BigWigS)

if (CURL_FOUND)
    include_directories(${CURL_INCLUDE_DIRS})
    target_link_libraries(BigWig ${CURL_LIBRARIES})
else()
    add_definitions(-DNOCURL)
endif()
