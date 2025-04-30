#ifndef PLAYER
#define PLAYER
#include <string>
#include <iostream>
#include "IO.h"
#include <cmath>
#include <stdlib.h>
using namespace std;

class Player
{
private:
    //Attributes
    int level;
    string weapon_equipped;
    int pos_x;
    int pos_y;
public:
    string name;
    int health;
    int attack;
    int defense;
    
    //Constructor
    Player();
    Player(string player_name);
  
    int get_x();
    
    int get_y();
    
    void set_position(int x, int y);
    
    char player_input();
    
    void take_damage(int attack);
    int player_attack();
};

#endif