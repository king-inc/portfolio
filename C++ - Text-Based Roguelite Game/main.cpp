#include <iostream> 
#include "game.h"
#include "mainmenu.h"

int main(){
    
    string name = menu(); //Starts up with main menu where player sets his/her name.  
    Player player_obj(name); //Create's a player object with the player's name.
    
    Game game(player_obj); //Creates a new game with the player's name.
    game.game_loop("test.txt"); //Runs the game loop with the map file's name.
    return 0;
}