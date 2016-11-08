cmake_minimum_required(VERSION 3.3)
project(CppToolBox)

#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-arcs -ftest-coverage -g")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")
aux_source_directory(. SRC_LIST)
aux_source_directory(./src SRC_LIST)
aux_source_directory(./tests SRC_LIST)
INCLUDE_DIRECTORIES(inc)

if (${CMAKE_SYSTEM_NAME} MATCHES "Windows")
    set(ENV{GTEST_ROOT} "C:/Program Files (x86)/googletest-distribution/")
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MT")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MTd")
    FIND_PACKAGE(GTest REQUIRED)
    INCLUDE_DIRECTORIES(${GTEST_INCLUDE_DIRS})
endif (${CMAKE_SYSTEM_NAME} MATCHES "Windows")

if (${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    INCLUDE_DIRECTORIES(/Users/raof01/workspace/gTest/gmock-1.7.0/gtest/include)
    LINK_DIRECTORIES(/Users/raof01/workspace/gTest/gmock-1.7.0/gtest/lib)
    SET(GTEST_LIBRARY gtest)
    SET(GTEST_MAIN_LIBRARY gtest_main)
endif (${CMAKE_SYSTEM_NAME} MATCHES "Darwin")

if (${CMAKE_SYSTEM_NAME} MATCHES "Linux")
    FIND_PACKAGE(GTest REQUIRED)
    INCLUDE_DIRECTORIES(${GTEST_INCLUDE_DIRS})
endif (${CMAKE_SYSTEM_NAME} MATCHES "Linux")

FIND_PACKAGE(Threads REQUIRED)

add_executable(${PROJECT_NAME} ${SRC_LIST})
target_link_libraries(${PROJECT_NAME} ${GTEST_LIBRARY} ${GTEST_MAIN_LIBRARY} ${CMAKE_THREAD_LIBS_INIT})
set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD 11)

# Copy Files
add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
                   COMMAND ${CMAKE_COMMAND} -E copy_directory
                       ${CMAKE_SOURCE_DIR}/tests/test_data $<TARGET_FILE_DIR:${PROJECT_NAME}>)
