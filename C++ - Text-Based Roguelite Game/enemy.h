#ifndef ENEMY
#define ENEMY
#include <vector>
#include <algorithm> //Used for square root and min functions.
#include "player.h"
#include <iostream>
class Enemy{
    
    private:
	int x;
	int y;
    char character;
    
    public:
    int health;
    int attack;
    int defense;
    std::string name;
        
    //Constuctor
    Enemy(char enemy_char, int _health,int _attack, int _defense,std::string _name) 
        : character(enemy_char), health(_health), attack(_attack), defense(_defense), name(_name) {};
    
    char get_char(){return character;} //Return's the enemy's character.
    int get_enemy_x(){return x;} // Returns x coordinate.
	int get_enemy_y(){return y;} // Returns y coordinate.
	void set_enemypos(int _x, int _y); // Set's enemy x and y coordinates.
    char enemy_move(std::vector<std::string> map_data, std::vector<std::vector<int>> graph, Player &player); //Makes enemy's move based on player's position.
    int enemy_attack(); //Returns an int representing attack strength.
    void take_damage(int attack); //Reduces health according to strength of attack taken.
};


//Below: Different types of enemies.
class Orc : public Enemy{
    public:
    Orc() : Enemy('o',20,4,10,"Orc"){}
};



class HighOrc : public Enemy
{
public:
    HighOrc():Enemy('H',30,5,15,"High Orc"){}
};



class Undead : public Enemy{
    public:
    Undead() : Enemy('u',5,1,10,"Undead"){}
};



class UndeadKing : public Enemy
{
public:
    UndeadKing():Enemy('K',15,2,5,"Undead King"){}
};



class Lizardman : public Enemy{
    public:
    Lizardman() : Enemy('l',5,10,15,"Lizardman"){}
};



class Dragon : public Enemy
{
public:
    Dragon():Enemy('D',60,12,25,"Dragon"){}
};


#endif