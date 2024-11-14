cmake_minimum_required(VERSION 3.21)
project(pyasmer C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 17)

find_package(Python3 COMPONENTS Interpreter Development)

message(STATUS "Python3_EXECUTABLE: ${Python3_EXECUTABLE}")
message(STATUS "Python3_INCLUDE_DIRS: ${Python3_INCLUDE_DIRS}")
message(STATUS "Python3_LIBRARIES: ${Python3_LIBRARIES}")
message(STATUS "Python3_LIBRARY_DIRS: ${Python3_LIBRARY_DIRS}")

find_package(pybind11 REQUIRED PATHS ${Python3_SITELIB})

message(STATUS "pybind11_VERSION: ${pybind11_VERSION}")
message(STATUS "pybind11_INCLUDE_DIRS: ${pybind11_INCLUDE_DIRS}")
message(STATUS "pybind11_DEFINITIONS: ${pybind11_DEFINITIONS}")

function(py_bind_module library_name source_files library_dep output_name)
    add_library(${library_name} SHARED ${source_files})
    target_include_directories(
            ${library_name}
            PUBLIC
            ${CMAKE_CURRENT_SOURCE_DIR}
            ${PROJECT_SOURCE_DIR}/include
            ${Python3_INCLUDE_DIRS})
    target_link_libraries(
            ${library_name}
            PRIVATE
            ${library_dep}
            pybind11::headers
            ${Python3_LIBRARIES})
    # target_link_options(${library_name} PRIVATE -static-libgcc -static-libstdc++)
    set_target_properties(${library_name} PROPERTIES PREFIX "")
    set_target_properties(${library_name} PROPERTIES OUTPUT_NAME ${output_name})
    set_target_properties(${library_name} PROPERTIES SUFFIX ".so")
endfunction()

set(sources
    src/pyasmer.c
)
py_bind_module(_pyasmer "${sources}" "" "_pyasmer")
