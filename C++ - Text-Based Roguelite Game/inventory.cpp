#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
#include "inventory.h"
using namespace std;

Inventory::Inventory() //constructor
{
}

string Inventory::add(string item) //adds an item to inventory
{
    allItems.push_back(item); //adds the specified item to the back of the vector
    std::cout<<"Added " <<item<<" to inventory.";
    return item;
}

string Inventory::remove(string item) //removes an item from the inventory
{
    allItems.erase(std::remove(allItems.begin(), allItems.end(), item), allItems.end()); //removes any elements that meet a criteria (item) within a range (start and end)
    std::cout<<"Tossed " <<item<<" away.";
}

void Inventory:: display() //show number of items in inventory
{
    std::cout<< "You have " << allItems.size() << " items."; //outputs the total size of the vector.
}
