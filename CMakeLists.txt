cmake_minimum_required(VERSION 3.21)
project(pyasmer C)

set(CMAKE_C_STANDARD 99)

if(NOT DEFINED PYTHON_PREFIX_PATH)
    message(FATAL_ERROR "PYTHON_PREFIX_PATH should be define")
endif()

set(PYTHON_CONFIG "${PYTHON_PREFIX_PATH}/bin/python3-config")
set(INCLUDE_ARGUMENT "--includes")
execute_process(
        COMMAND ${PYTHON_CONFIG} ${INCLUDE_ARGUMENT}
        OUTPUT_VARIABLE PYTHON_INCLUDES
)
string(REPLACE "\n" "" PYTHON_INCLUDES ${PYTHON_INCLUDES})
string(REPLACE "/" ";" PYTHON_INCLUDES_STRINGS ${PYTHON_INCLUDES})
list(GET PYTHON_INCLUDES_STRINGS -1 PYTHON_VERSION)
message(STATUS "VERSION = ${PYTHON_VERSION}")

set(LDFLAGS_ARGUMENT "--ldflags")
execute_process(
        COMMAND ${PYTHON_CONFIG} ${LDFLAGS_ARGUMENT}
        OUTPUT_VARIABLE PYTHON_LDFLAGS
)
string(REPLACE "\n" "" PYTHON_LDFLAGS ${PYTHON_LDFLAGS})
string(STRIP ${PYTHON_LDFLAGS} PYTHON_LDFLAGS)
message(STATUS "LDFLAGS = ${PYTHON_LDFLAGS}")

include_directories(
        ${PYTHON_PREFIX_PATH}/include/${PYTHON_VERSION}
        ${CMAKE_SOURCE_DIR}/include
)

file(GLOB NATIVE_FILES src/*.c)

add_library(_pyasmer SHARED ${NATIVE_FILES})
target_link_libraries(_pyasmer "${PYTHON_LDFLAGS}")
set_target_properties(_pyasmer PROPERTIES PREFIX "")
