cmake_minimum_required(VERSION 3.8)
project(oradar_lidar)

set(CMAKE_CXX_STANDARD 14)
add_compile_options(-O3)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)

# Required: enables the ROS2 code path in oradar_scan_node.cpp,
# which uses #ifdef ROS2_FOUND guards throughout.
add_definitions(-DROS2_FOUND)

set(ORADAR_SDK_DIR "sdk")
add_subdirectory(${ORADAR_SDK_DIR})

include_directories(
  ${CMAKE_CURRENT_SOURCE_DIR}/include
  ${CMAKE_CURRENT_SOURCE_DIR}/${ORADAR_SDK_DIR}
)

add_executable(oradar_scan src/oradar_scan_node.cpp)

ament_target_dependencies(oradar_scan rclcpp sensor_msgs)
target_link_libraries(oradar_scan oradar_sdk pthread)

install(TARGETS oradar_scan
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch/ rviz2/
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
