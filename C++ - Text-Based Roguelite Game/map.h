#ifndef MAP
#define MAP
#include <fstream> //Used for ifstream function to read text file for map loading.
#include <iostream>
#include <vector>
#include "player.h"
#include "enemy.h"
#include <algorithm> //Used for square root and round functions.
#include "Battle.h"
class Map{
    public:
    int width = 1; //Width of map (set when map is loaded in).
    int height = 1; //Height of map (set when map is loaded in).
    std::string input; //Temporarily stores each line that is read from the text file before it is pushed back into the map data vector
    std::vector<std::string> map_data; //Stores the map data.
	std::vector<vector<int>> graph; //Dijkstra map that is used for pathfinding.
	
    void load_map(std::string map_file, Player &player, std::vector<Enemy>& enemies); //Loads the map into the map data vector.
	void generate_graph(Player &player); //Calculates the dijkstra map according to the player's position.
    void print_map(); //Prints the map onto the screen.
    void move_player(Player &player); //Draws player in new position according to player input.
	void move_enemy(std::vector<Enemy>& enemies, Player &player); //Draws enemy in new position according to enemy input.
};




#endif