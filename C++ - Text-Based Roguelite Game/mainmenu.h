#include <iostream>
#include "IO.cpp"

using namespace std;

string menu()
{
    system("clear");
    string choice;
    cout << "Welcome to Ruin Explorer!" << endl;
    cout << "-Press Enter to Start" << endl;
    cout << "-Press Space for Instructions" << endl;
    cout << "-Press Esc to Quit" << endl;
    bool stop = false;
    
    while( stop == false )
    {
        int input = mygetch();
        if( input == 10 )
        {
            stop = true;
            string name;
            cout << "************************" << endl;
            cout << "Please input your player name: ";
            cin >> name;
            return name;
        }
        else if( input == 32 )
        {
            stop = true;
            cout << "************************" << endl;
            cout << "Controls:" << endl;
            cout << "-W A S D to move" << endl;
            cout << "-Enter to attack" << endl;
            cout << "-Esc to Quit" << endl;
            cout << "************************" << endl;
            input = mygetch();
            string name = menu();
            return name;
        }
        else if( input == 27 )
        {
            stop = true;
            cout << "Exiting..." << endl;
            exit(0);
        }
    }
}