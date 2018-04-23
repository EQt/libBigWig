include(ExternalProject)

find_package(ZLIB)

if (NOT ZLIB_FOUND)
  message(STATUS "compiling ZLIB myself")

  set(LIBZ_INSTALL_DIR ${CMAKE_BINARY_DIR})
  externalProject_Add(zlib
    PREFIX  ${PROJECT_BINARY_DIR}/zlib
    URL     http://zlib.net/zlib-1.2.8.tar.gz
    URL_MD5 44d667c142d7cda120332623eab69f40
    UPDATE_COMMAND ""
    DOWNLOAD_DIR ${LIBZ_PREFIX}
    SOURCE_DIR   ${LIBZ_PREFIX}/libz-1.2.8
    CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=${LIBZ_INSTALL_DIR}
               -DBUILD_TYPE=Release
               -DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}
               -DCMAKE_C_COMPILER=${CMAKE_C_COMPILER}
  )
  # set_property(TARGET zlib PROPERTY FOLDER "extern")

  if (MSVC)
    set(ZLIBLIBNAME zlibstatic${POSTFIX}.lib)
    set(zlib_shared ${LIBZ_INSTALL_DIR}/lib/zlib${POSTFIX}.lib)
  else(MINGW)
    set(ZLIBLIBNAME libzlibstatic.a)
    set(zlib_shared ${LIBZ_INSTALL_DIR}/lib/libzlib.dll.a)
  else()
    set(ZLIBLIBNAME ${CMAKE_STATIC_LIBRARY_PREFIX}zlib${CMAKE_STATIC_LIBRARY_SUFFIX})
    message(ERROR "FindLibZ not configured for this case")
  endif()
  set(ZLIB_INCLUDE_DIR ${LIBZ_INSTALL_DIR}/include)
  set(ZLIB_LIBRARY     ${LIBZ_INSTALL_DIR}/lib/${ZLIBLIBNAME})

  externalProject_Add_Step(zlib remove_shared_zlib
    DEPENDEES install
    COMMAND ${CMAKE_COMMAND} -E remove ${zlib_shared}
    COMMENT "Removing shared zlib (because we want the static version)"
  )
  externalProject_Add_Step(zlib copy_static_zlib
    DEPENDEES remove_shared_zlib
    COMMAND ${CMAKE_COMMAND} -E copy ${ZLIB_LIBRARY} ${zlib_shared}
    COMMENT "Rename zlib from ${ZLIB_SHARED} to ${zlib_shared}"
  )
endif()
