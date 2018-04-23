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

if (CURL_FOUND)
    include_directories(${CURL_INCLUDE_DIRS})
    target_link_libraries(BigWig ${CURL_LIBRARIES})
else()
    add_definitions(-DNOCURL)
endif()
