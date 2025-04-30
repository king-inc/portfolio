cmake_minimum_required(VERSION 3.0)
set(CMAKE_CXX_STANDARD 14)

project(Hangman CXX)

# turns out that g++ will allow variable length arrays but I 
# dont' want students getting dependant on non-standard features
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wvla -Werror=vla")

# limit number of errors shown to 1
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wfatal-errors")

# location of source code files
include_directories(${CMAKE_SOURCE_DIR})

# tell cmake where to put the executables that it creates
file(MAKE_DIRECTORY ${CMAKE_SOURCE_DIR}/bin)    
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin ) 

# where to put the object files it creates
file(MAKE_DIRECTORY ${CMAKE_SOURCE_DIR}/lib)
SET(LIBRARY_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/lib)

add_library(Battle Battle.cpp)
add_library(map map.cpp)
add_library(IO IO.cpp)
add_library(player player.cpp)
add_library(game game.cpp)
add_library(enemy enemy.cpp)

add_executable( main main.cpp )

target_link_libraries(main game player map IO enemy Battle)
