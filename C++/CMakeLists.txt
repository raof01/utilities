cmake_minimum_required(VERSION 3.3)
project(CppToolBox)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

aux_source_directory(. SRC_LIST)
aux_source_directory(./src SRC_LIST)
aux_source_directory(./tests SRC_LIST)

INCLUDE_DIRECTORIES(inc
        /Users/raof01/workspace/gTest/gmock-1.7.0/gtest/include)

LINK_DIRECTORIES(/Users/raof01/workspace/gTest/gmock-1.7.0/gtest/lib)

add_executable(${PROJECT_NAME} ${SRC_LIST})

target_link_libraries(${PROJECT_NAME} gtest gtest_main)
