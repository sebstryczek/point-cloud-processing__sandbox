cmake_minimum_required(VERSION 3.10)

project(HelloWorld)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_VERBOSE_MAKEFILE on)

set(EIGEN3_INCLUDE_DIR "${CMAKE_SOURCE_DIR}/libs/Eigen/src")
include_directories(${EIGEN3_INCLUDE_DIR})

find_package(Open3D REQUIRED)

add_executable(HelloWorld
    ../src/main.cpp
    ../libs/hough3d/vector3d.cpp
    ../libs/hough3d/pointcloud.cpp
    ../libs/hough3d/hough.cpp
    ../libs/hough3d/sphere.cpp
)

# find_package(Boost REQUIRED)
# target_link_libraries(HelloWorld PRIVATE Boost::boost)
target_link_libraries(HelloWorld PRIVATE Open3D::Open3D)
