#include "player.h"

Player::Player(){
    //Default Constructor
}
Player::Player(string player_name){
    name = player_name;
    health = 50;
    attack = 10;
    level = 1;
    defense = 5;
    weapon_equipped =  "none";
}


int Player::get_x(){
    return pos_x;
}

int Player::get_y(){
    return pos_y;
}

void Player::set_position(int x, int y){
    pos_x = x;
    pos_y = y;
}

char Player::player_input(){
    char _key;
    int key = mygetch();
    switch( key )
    {
        case 119:
            _key = 'w';
            break;
        case 97:
            _key = 'a';
            break;
        case 100:
            _key = 'd';
            break;
        case 115:
            _key = 's';
            break;
        case 27:
            _key = '/';
            break;
    }
    return _key;
}


int Player::player_attack(){
    return rand() % attack;
}
void Player::take_damage(int attack){
     health -= round(attack - attack/defense);
}