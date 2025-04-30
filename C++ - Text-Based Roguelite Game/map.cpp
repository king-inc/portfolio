#include "map.h"

void Map::load_map(std::string map_file, Player &player, std::vector<Enemy>& enemies){
  
    std::ifstream file(map_file); //Reads text document with set file name.
    std::string input; 
    
    //While the file is being read, each line is pushed back into the map data vector.
    while(getline(file, input)){
        map_data.push_back(input);
        height++; //Increments map height value by 1 to set map height.
        }
    
    
    //Goes through each tile of the map and checks if the tile is a game object like player or enemy.
    for(int i = 0; i < map_data.size(); i++){
        for(int j = 0; j < map_data[i].size(); j++){
            
            char tile = map_data[i][j];                
            switch(tile){
                case '@':
                {
                    player.set_position(j, i); //In the case that the player is detected, the player's position is set according to position on the map.
                    break;
                }
                
                //Below: If enemy characters are detected, a new enemy object is made and is pushed back into the 'enemies' vector that stores all of the enemies on the map.
				case 'o':
                {
					Orc newOrc;
                    newOrc.set_enemypos(j,i);
                    enemies.push_back(newOrc);
                    break;
                }
                case 'u':
                {    
                    Undead newUndead;
                    newUndead.set_enemypos(j,i);
                    enemies.push_back(newUndead);
                    break;
                }
                case 'l':
                {
                    Lizardman newLizardman;
                    newLizardman.set_enemypos(j,i);
                    enemies.push_back(newLizardman);
                    break;
                }
            }
        }
    }
  width = map_data[1].size(); //Set's the map's width according to the first line of the map (assumes the map is a rectangle)
    

  graph.resize(height, std::vector<int>(width, 0)); //Initialises dijkstra graph with all values set to 0 according to height and width of the map.
}


void Map::print_map(){
    for(std::string i: map_data){
        std::cout << i << std::endl;
    }
}


void Map::move_player(Player &player){
    char input = player.player_input(); //Gets the player input.
    
    //Gets player's x and y coordinates and stores them.
    int x = player.get_x();
    int y = player.get_y();

    
//Based on the player's input, the map will draw the player in its new position, and set its previous position to a '.' before the map refreshes.
switch(input){
        case 'w':
        if(map_data[y-1][x] == '.'){ 
            map_data[y][x] = '.';
            map_data[y-1][x]  = '@';
            player.set_position(x, y-1);
        }
        break;

        case 's':
        if(map_data[y + 1][x] == '.'){ 
            map_data[y][x] = '.';
            map_data[y + 1][x]  = '@';
            player.set_position(x, y + 1);
        }
        break;

        case 'a':
        if(map_data[y][x - 1] == '.'){ 
            map_data[y][x] = '.';
            map_data[y][x - 1]  = '@';
            player.set_position(x - 1, y);
        }
        break;

        case 'd':
        if(map_data[y][x + 1] == '.'){ 
        map_data[y][x] = '.';
        map_data[y][x + 1]  = '@';
        player.set_position(x + 1, y);
        }
        break;
        
        case '/':
        std::cout<<"Press Esc again to exit"<<std::endl;
        int inp = mygetch();
        if(inp == 27){
        exit(0);
        }
        break;
    }
}



void Map::generate_graph(Player &player){
    
    //Calculates weight for each note of the graph, with the player's position as starting point
    for(int i = 0; i < map_data.size(); i++){
        for(int j = 0; j < map_data[i].size(); j++){
            int tilex = j;
            int tiley = i;
            int playerx = player.get_x();
            int playery = player.get_y();
        
        //If it encounters a wall, it sets the value of the wall to 999 in order to stop enemy from colliding with walls and avoid them.
        if(map_data[i][j] == '#'){
            graph[i][j] = 999;
         
        } else { 
            int distance = round(sqrt(pow((tiley - playery), 2) + pow((tilex - playerx), 2))); //Calculates the distance of tile from the player.
            graph[i][j] = distance; //Set's the corresponding graph value to the calculated value.            
        }
}
}
}


void Map::move_enemy(std::vector<Enemy>& enemies, Player &player){
    
    //Goes through each enemy and moves them.
    for(int i = 0; i < enemies.size(); i++){
        int x = enemies[i].get_enemy_x();
        int y = enemies[i].get_enemy_y();
        char move = enemies[i].enemy_move(map_data, graph, player); //Get's the enemy's input.
        char character = enemies[i].get_char(); //Get's the enemy's character to draw it into the new position.
        
        //Works exactly the same way as them move_player() function. Except when the enemy encounters a player, it starts a battle event.
        switch(move){
        case 'd':
            map_data[y][x] = '.';
            map_data[y][x + 1]  = character;
            enemies[i].set_enemypos(x+1, y);    
            break;
            
        case 'a':
            map_data[y][x] = '.';
            map_data[y][x - 1]  = character;
            enemies[i].set_enemypos(x-1, y); 
            break;
            
        case 's':
            map_data[y][x] = '.';
            map_data[y + 1][x]  = character;
            enemies[i].set_enemypos(x, y+1); 
            break;
            
        case 'w':
            map_data[y][x] = '.';
            map_data[y-1][x]  = character;
            enemies[i].set_enemypos(x, y - 1); 
            break;
            
        case 'c':
            map_data[y][x] = '.';
            map_data[y + 1][x + 1] = character;
            enemies[i].set_enemypos(x+1, y+1);
            break;
            
        case 'q':
            map_data[y][x] = '.';
            map_data[y - 1][x - 1] = character;
            enemies[i].set_enemypos(x - 1, y - 1);
            break;
            
        case 'e':
            map_data[y][x] = '.';
            map_data[y - 1][x + 1] = character;
            enemies[i].set_enemypos(x+1, y - 1); 

            break;
            
        case 'z':
            map_data[y][x] = '.';
            map_data[y + 1][x - 1] = character;
            enemies[i].set_enemypos(x-1, y+1); 
            break;
                
        case 'b':
            Battle(player, enemies[i]);
            
            //If after the battle, the enemy's health is less than or equal to 0, the enemy object will be deleted, and its character will be replaced with a '.'
            if (enemies[i].health <= 0){
                map_data[y][x] = '.';
                enemies.erase(enemies.begin() + i, enemies.begin() + (i+1));
            }
            break;
    }
    }
}
