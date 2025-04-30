#ifndef GAME 
#define GAME
#include <iostream>
#include "map.h"
#include "player.h"
#include "enemy.h"
#include <stdlib.h>
class Game{
    
    public:
    Map map; //Responsible for all map data and drawing objects onto screen.
    Player player; //Responsible for player.
    std::vector<Enemy> enemies; //Stores all of the enemies on the map.
    
    Game(Player player_obj); //Constructor.
    
    void game_loop(std::string map_file); //Contains game loop.
    
};




#endif