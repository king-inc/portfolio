#include "Battle.h"

//Battle function
//Edited some code from https://cplusplus.happycodings.com/games/code11.html
void Battle(Player &player, Enemy &enemy)
{

      
      std::cout << player.name << "\'s " << "health: " << player.health << std::endl;
      std::cout << enemy.name << " health: " << enemy.health << std::endl;
      
      std::cout << "-Press enter to attack " << std::endl;
      int input = mygetch();
      
      if(input == 10){
          int attack = player.player_attack();
          
          if(attack == 0){
              std::cout << "You missed!" << std::endl;
          }
          std::cout << "You attacked!" << std::endl;
          enemy.take_damage(attack);
      }
      
      int e_attack = enemy.enemy_attack();
      std::cout << enemy.name << " attacked!" << std::endl;
      player.take_damage(e_attack);
      cout << "**********************" << endl;
      
      
 
}