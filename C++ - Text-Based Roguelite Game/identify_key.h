#include <iostream>
#include "IO.cpp"

using namespace std;

string return_keys()
{
    string _key;
    int key = mygetch();
    switch( key )
    {
        case 119:
            _key = "w";
            break;
        case 97:
            _key = "a";
            break;
        case 100:
            _key = "d";
            break;
        case 115:
            _key = "s";
            break;
        case 27:
            _key = "Esc";
            break;
        case 10:
            _key = "Enter";
            break;
        case 127:
            _key = "BackSpace";
            break;
        case 32:
            _key = "Space";
            break;
        default:
            cout<<"Use WASD to move";        
    }
    return _key;
}