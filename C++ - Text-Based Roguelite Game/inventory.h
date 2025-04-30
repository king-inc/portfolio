#include <iostream>
#include <string>
#include <vector>
using namespace std;

class Inventory
{
    public:
        Inventory(); //constructor
        void display();
        string add(string item);
        string remove(string item);
    private:
        vector<string> allItems;
        
};