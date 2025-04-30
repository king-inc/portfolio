#include "game.h"
#inlcude "damagepotion.cpp"

Game::Game(Player player_obj){
    player = player_obj; //Set's up player object.
}

void Game::game_loop(std::string map_file){
   level.load_map(map_file, player, enemies);

while(true){
   //If the player health is <=0 player is presented with a game over screen. 
   if(player.health <= 0){
       std::cout << "GAME OVER" << std::endl;
       exit(0);
   //If all of the enemies have been killed, the player is presented with a 'YOU WIN' screen.
   } else if (enemies.size() == 0){
       std::cout << "YOU WIN" << std::endl;
       exit(0);
   }
    
   map.generate_graph(player);
   map.print_map();
   std::cout << "Health: " << player.health << std::endl;
   level.move_player(player);
   level.move_enemy(enemies, player);
   system("clear"); //Used to clear screen.
}
}


