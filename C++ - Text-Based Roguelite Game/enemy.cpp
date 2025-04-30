#include "enemy.h"

void Enemy::set_enemypos(int _x, int _y){
	x = _x;
	y = _y;
}

char Enemy::enemy_move(std::vector<std::string> map_data, std::vector<std::vector<int>> graph, Player &player){
    
    //Get's player's x and y coordinates for distance calculation.
    int playerx = player.get_x();
    int playery = player.get_y();
    
    //Get's the enemy's current x and y coordinate for distance calculation.
    int x = get_enemy_x();
    int y = get_enemy_y();
    
    
    int player_distance = round(sqrt(pow((y - playery), 2) + pow((x - playerx), 2))); //Calculates distance of player from the enemy.
    
    std::vector<int> options; //Stores potential moves for the enemy.
    
    //Pushes back the weights of the nodes immediately surrounding the enemy on the dijkstra graph.
    options.push_back(graph[y][x + 1]); 
    options.push_back(graph[y][x - 1]);
    options.push_back(graph[y+1][x]);
    options.push_back(graph[y-1][x]);
    options.push_back(graph[y + 1][x + 1]);
    options.push_back(graph[y - 1][x - 1]);
    options.push_back(graph[y - 1][x + 1]);
    options.push_back(graph[y + 1][x - 1]);
    
    
    int min = *min_element(options.begin(), options.end()); //Determines the minimum element from the list of node weights.
    std::vector<char> outputs {'w', 'a', 's', 'd', 'q', 'e', 'z', 'c'}; //A set of predefined moves for the enemy to randomly chose from (given player is not within range).
    
    if (player_distance < 12){ // If the player is within a certain set distance, the enemy will start pathfinding.
        
        //Checks if the node that the enemy wants to move to has the minimum weight. 
        //If it does, the enemy will return the input corresponding to that move. (if the tile that the enemy wants to move to is the player, it returns 'b' to attack).
            if(graph[y][x+1] == min){
                if(map_data[y][x+1] == '.'){
                    return 'd';
                } else if (map_data[y][x+1] == '@') {
                    return 'b';
                }
            }
                
            else if (graph[y][x-1] == min){
                if(map_data[y][x-1] == '.'){      
                    return 'a';
                } else if (map_data[y][x-1] == '@') {
                    return 'b';
                }
            }
            
                
            else if (graph[y+1][x] == min){
                if(map_data[y+1][x] == '.'){
                    return 's';
                } else if (map_data[y+1][x] == '@') {
                    return 'b';
                }
            }
                
                
            else if (graph[y-1][x] == min){
                if(map_data[y-1][x] == '.'){
                    return 'w';
                } else if (map_data[y-1][x] == '@') {
                    return 'b';
                }
            }
                
                
            else if (graph[y-1][x-1] == min){
                if(map_data[y-1][x-1] == '.'){
                    return 'q';
                } else if (map_data[y-1][x-1] == '@') {
                    return 'b';
                }
            }

                
            else if (graph[y+1][x+1] == min){
                if(map_data[y+1][x+1] == '.'){
                    return 'c';
                } else if (map_data[y + 1][x+1] == '@') {
                    return 'b';
                }
            }

                
            else if (graph[y-1][x+1] == min){
                if(map_data[y-1][x+1] == '.'){
                    return 'e';
                } else if (map_data[y - 1][x+1] == '@') {
                    return 'b';
                }
            }

                
            else if (graph[y+1][x-1] == min){
                if(map_data[y+1][x-1] == '.'){
                    return 'z';    
                } else if (map_data[y+1][x-1] == '@') {
                    return 'b';
                }
            }
        }
    
    //If the player is not within range, it will randomly chose from the set of inputs that I had defined earlier.
    else { 
       int randnum = rand() % 7;
       char choice = outputs[randnum]; 
       
        if(choice == 'd'){
            if(map_data[y][x+1] == '.'){
                return 'd';
            }
        }

        else if (choice == 'a'){
            if(map_data[y][x-1] == '.'){
                return 'a';
            }
        }


        else if (choice == 's'){
            if(map_data[y+1][x] == '.'){
                return 's';
            }
        }


        else if (choice == 'w'){
            if(map_data[y-1][x] == '.'){
                return 'w';
            }
        }


        else if (choice == 'q'){
            if(map_data[y-1][x-1] == '.'){
                return 'q';
            }
        }


        else if (choice == 'c'){
            if(map_data[y+1][x+1] == '.'){
                return 'c';
            }
        }


        else if (choice == 'e'){
            if(map_data[y-1][x+1] == '.'){
                return 'e';
            }
        }


        else if (choice == 'z'){
            if(map_data[y+1][x-1] == '.'){
                return 'z';    
            }
        }

    }
}

int Enemy::enemy_attack(){
    return rand() % attack; //Selects a random attack value between 0 and the enemy's attack stat.
}
void Enemy::take_damage(int attack){
     health -= round(attack - (attack/defense)); //Calculates the amount of damage done and subtracts from health.
}