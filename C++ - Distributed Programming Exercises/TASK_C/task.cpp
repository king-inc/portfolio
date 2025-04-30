#include <iostream>
#include <string>    
#include <cstring>
#include "mpi.h"

typedef struct {
  float list[15];
  int size;
  char letter;
  double number;
  int x;
  int y;
} ExampleStruct1;

MPI::Datatype  mpiStruct1(){
    //how many data types in the struct
    const int count = 6; 
    //type of every different block of data
    MPI::Datatype typesInStruct[count] = {MPI::FLOAT,MPI::INT,MPI::CHAR,MPI::DOUBLE,MPI::INT,MPI::INT};
    //how many elements per block 
    int arrayBlockLengths [count] = {15,1,1,1,1,1};
    //Now we need to specify starting memory location of each block, *relative to the start of the struct only*
    // it's a bit of a tedious process, but neccesary. 
    MPI::Aint objAddress, address1,address2,address3,address4,address5,address6;
    MPI::Aint arrayDisplacements[count];	
    ExampleStruct1 sbuf;//Just has to be a struct instance but not
                    // the one you're actually sending, since we only need those locations,
                    // which, since this is a static struct, will always be the same
    objAddress = MPI::Get_address(&sbuf);
    address1 = MPI::Get_address(&sbuf.list);
    address2 = MPI::Get_address(&sbuf.size);
    address3 = MPI::Get_address(&sbuf.letter);
    address4 = MPI::Get_address(&sbuf.number);
    address5 = MPI::Get_address(&sbuf.x);
    address6 = MPI::Get_address(&sbuf.y);
    arrayDisplacements[0] = address1 - objAddress;
    arrayDisplacements[1] = address2 - objAddress;
    arrayDisplacements[2] = address3 - objAddress;
    arrayDisplacements[3] = address4 - objAddress;
    arrayDisplacements[4] = address5 - objAddress;
    arrayDisplacements[5] = address6 - objAddress;
    // now we create the MPI equivilent datatype using the data we just collected
    MPI::Datatype mpiHostStruct;
    mpiHostStruct = MPI::Datatype::Create_struct(count,arrayBlockLengths,arrayDisplacements,typesInStruct);
    // and commit it the the Communicator, so it can be used accross the entire cluster
    mpiHostStruct.Commit();
    return mpiHostStruct;
  }
  
typedef struct {
  int playerlist[30];
  int playerlistSize;
  char levelName[50];
  int levelNameSize;
  long double randVar;
  int gameBoardWidth;
  int gameBoardHeight;  
} ExampleStruct2;

MPI::Datatype  mpiStruct2(){
    //how many data types in the struct
    const int count = 7; 
    //type of every different block of data
    MPI::Datatype typesInStruct[count] = {MPI::INT,MPI::INT,MPI::CHAR,MPI::INT,MPI::LONG_DOUBLE,MPI::INT,MPI::INT};
    //how many elements per block 
    int arrayBlockLengths [count] = {30,1,50,1,1,1,1};
    //Now we need to specify starting memory location of each block, *relative to the start of the struct only*
    // it's a bit of a tedious process, but neccesary. 
    MPI::Aint objAddress, address1,address2,address3,address4,address5,address6,address7;
    MPI::Aint arrayDisplacements[count];	
    ExampleStruct2 sbuf;//Just has to be a struct instance but not
                    // the one you're actually sending, since we only need those locations,
                    // which, since this is a static struct, will always be the same
    objAddress = MPI::Get_address(&sbuf);
    address1 = MPI::Get_address(&sbuf.playerlist);
    address2 = MPI::Get_address(&sbuf.playerlistSize);
    address3 = MPI::Get_address(&sbuf.levelName);
    address4 = MPI::Get_address(&sbuf.levelNameSize);
    address5 = MPI::Get_address(&sbuf.randVar);
    address6 = MPI::Get_address(&sbuf.gameBoardWidth);
    address7 = MPI::Get_address(&sbuf.gameBoardHeight);
    arrayDisplacements[0] = address1 - objAddress;
    arrayDisplacements[1] = address2 - objAddress;
    arrayDisplacements[2] = address3 - objAddress;
    arrayDisplacements[3] = address4 - objAddress;
    arrayDisplacements[4] = address5 - objAddress;
    arrayDisplacements[5] = address6 - objAddress;
    arrayDisplacements[6] = address7 - objAddress;
    // now we create the MPI equivilent datatype using the data we just collected
    MPI::Datatype mpiHostStruct;
    mpiHostStruct = MPI::Datatype::Create_struct(count,arrayBlockLengths,arrayDisplacements,typesInStruct);
    // and commit it the the Communicator, so it can be used accross the entire cluster
    mpiHostStruct.Commit();
    return mpiHostStruct;
  }
  
typedef struct {
  char playerName[100];
  int playerNameSize;
  float playerHealth;
  float playerMana;
  char itemList[50];
  int itemListSize;
  double warewolfPercentage;
} ExampleStruct3;

MPI::Datatype  mpiStruct3(){
    //how many data types in the struct
    const int count = 7; 
    //type of every different block of data
    MPI::Datatype typesInStruct[count] = {MPI::CHAR,MPI::INT,MPI::FLOAT,MPI::FLOAT,MPI::CHAR,MPI::INT,MPI::DOUBLE};
    //how many elements per block 
    int arrayBlockLengths [count] = {100,1,1,1,50,1,1};
    //Now we need to specify starting memory location of each block, *relative to the start of the struct only*
    // it's a bit of a tedious process, but neccesary. 
    MPI::Aint objAddress, address1,address2,address3,address4,address5,address6,address7;
    MPI::Aint arrayDisplacements[count];	
    ExampleStruct3 sbuf;//Just has to be a struct instance but not
                    // the one you're actually sending, since we only need those locations,
                    // which, since this is a static struct, will always be the same
    objAddress = MPI::Get_address(&sbuf);
    address1 = MPI::Get_address(&sbuf.playerName);
    address2 = MPI::Get_address(&sbuf.playerNameSize);
    address3 = MPI::Get_address(&sbuf.playerHealth);
    address4 = MPI::Get_address(&sbuf.playerMana);
    address5 = MPI::Get_address(&sbuf.itemList);
    address6 = MPI::Get_address(&sbuf.itemListSize);
    address7 = MPI::Get_address(&sbuf.warewolfPercentage);
    arrayDisplacements[0] = address1 - objAddress;
    arrayDisplacements[1] = address2 - objAddress;
    arrayDisplacements[2] = address3 - objAddress;
    arrayDisplacements[3] = address4 - objAddress;
    arrayDisplacements[4] = address5 - objAddress;
    arrayDisplacements[5] = address6 - objAddress;
    arrayDisplacements[6] = address7 - objAddress;
    // now we create the MPI equivilent datatype using the data we just collected
    MPI::Datatype mpiHostStruct;
    mpiHostStruct = MPI::Datatype::Create_struct(count,arrayBlockLengths,arrayDisplacements,typesInStruct);
    // and commit it the the Communicator, so it can be used accross the entire cluster
    mpiHostStruct.Commit();
    return mpiHostStruct;
  }
  
int main(int argc, char** argv) {
    int com_size, world_rank, namelen;
    char node_name[MPI_MAX_PROCESSOR_NAME];
  
    MPI_Init(NULL,NULL);
  	MPI_Comm_size(MPI_COMM_WORLD, &com_size);
  	MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
  	memset(node_name, 0, MPI_MAX_PROCESSOR_NAME);
  	MPI_Get_processor_name(node_name, &namelen);
  	memset(node_name+namelen,0,MPI_MAX_PROCESSOR_NAME-namelen);
  	
  	// Create instances of the datatypes built
  	MPI::Datatype mpiHostStruct1 = mpiStruct1();
    MPI::Datatype mpiHostStruct2 = mpiStruct2();
    MPI::Datatype mpiHostStruct3 = mpiStruct3();
  
  	// nodes to use
  	int source = 0;
  	int destination = 1;

    // Sending data 
    if (world_rank == source){
        // make new struct types and initialise them with some data
        ExampleStruct1 example1 = { {0.5,0.2,0.3},3,'Q',2.5,54, 42 };
        ExampleStruct2 example2 = { {1,2,3},3,"dungeon",7,4.5,5,6};
        ExampleStruct3 example3 = { "hero",4,76.5,10.2,"health potion",13,17.2};
        
        //send them to the receiving node
        MPI_Send(&example1,1, mpiHostStruct1, destination, 0, MPI_COMM_WORLD);
        MPI_Send(&example2,1, mpiHostStruct2, destination, 0, MPI_COMM_WORLD);
        MPI_Send(&example3,1, mpiHostStruct3, destination, 0, MPI_COMM_WORLD);
        
        
        //make new struct types to store incoming data
        ExampleStruct1 recv_example1;
        //receive new data from destination node
        MPI_Recv(&recv_example1, 1, mpiHostStruct1,destination,0,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
         
        //print struct data
        std::cout<<"ExampleStruct1: "<< std::endl;
        std::cout << "NewList: " << recv_example1.list[0] << ", OriginalList: " << example1.list[0]<<std::endl;
        std::cout << "NewList: " << recv_example1.list[1]<< ", OriginalList: " << example1.list[1] <<std::endl;
        std::cout << "NewList: " << recv_example1.list[2]<< ", OriginalList: " << example1.list[2] <<std::endl;
        std::cout << "NewList: " << recv_example1.list[3]<< ", OriginalList: " << example1.list[3] <<std::endl;
        std::cout << "NewSize: " << recv_example1.size << ", OriginalSize: " << example1.size<< std::endl;
        std::cout << "NewLetter: " << recv_example1.letter << ", OriginalLetter: " << example1.letter<< std::endl;
        std::cout << "NewNumber: " << recv_example1.number << ", OriginalNumber: " << example1.number<< std::endl;
        std::cout << "NewX: " << recv_example1.x << ", OriginalX: " << example1.x<< std::endl;
        std::cout << "NewY: " << recv_example1.y << ", OriginalY: " << example1.y<< std::endl;
        //end line to seperate structs
        std::cout<<std::endl;
      
        //make new struct types to store incoming data
        ExampleStruct2 recv_example2;
        //receive new data from destination node
        MPI_Recv(&recv_example2, 1, mpiHostStruct2,destination,0,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
         
        //print struct data
        std::cout<<"ExampleStruct2: "<< std::endl;
        std::cout << "NewPlayerList: " << recv_example2.playerlist[0]<< ", OriginalPlayerList: " << example2.playerlist[0] <<std::endl;
        std::cout << "NewPlayerList: " << recv_example2.playerlist[1]<< ", OriginalPlayerList: " << example2.playerlist[1] <<std::endl;
        std::cout << "NewPlayerList: " << recv_example2.playerlist[2]<< ", OriginalPlayerList: " << example2.playerlist[2] <<std::endl;
        std::cout << "NewPlayerList: " << recv_example2.playerlist[3] << ", OriginalPlayerList: " << example2.playerlist[3]<<std::endl;
        std::cout << "NewPlayerListSize: " << recv_example2.playerlistSize<< ", OriginalPlayerListSize: " << example2.playerlistSize << std::endl;
        std::cout << "NewlevelName: " << recv_example2.levelName << ", OriginalLevelName: " << example2.levelName<< std::endl;
        std::cout << "NewRandVar: " << recv_example2.randVar<< ", OriginalRandVar: " << example2.randVar << std::endl;
        std::cout << "NewGameBoardWidth: " << recv_example2.gameBoardWidth << ", OriginalGameBoardWidth: " << example2.gameBoardWidth<< std::endl;
        std::cout << "NewGameBoardHeight: " << recv_example2.gameBoardHeight << ", OriginalGameBoardHeight: " << example2.gameBoardHeight<< std::endl;
        //end line to seperate structs
        std::cout<<std::endl;
        
        //make new struct types to store incoming data
        ExampleStruct3 recv_example3;
        //receive new data from destination node
        MPI_Recv(&recv_example3, 1, mpiHostStruct3,destination,0,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
        
        //print struct data
        std::cout<<"ExampleStruct3: "<< std::endl;
        std::cout << "NewPlayerName: " << recv_example3.playerName<< ", OriginalPlayerName: " << example3.playerName <<std::endl;
        std::cout << "NewPlayerNameSize: " << recv_example3.playerNameSize<< ", OriginalPlayerNameSize: " << example3.playerNameSize<< std::endl;
        std::cout << "NewPlayerHealth: " << recv_example3.playerHealth<< ", OriginalPlayerHealth: " << example3.playerHealth<< std::endl;
        std::cout << "NewPlayerMana: " << recv_example3.playerMana<< ", OriginalPlayerMana: " << example3.playerMana<< std::endl;
        std::cout << "NewItemList: " << recv_example3.itemList<< ", OriginalItemList: " << example3.itemList<< std::endl;
        std::cout << "NewItemListSize: " << recv_example3.itemListSize<<", OriginalItemListSize: " << example3.itemListSize << std::endl;
        std::cout << "NewWarewolfPercentage: " << recv_example3.warewolfPercentage<<", OriginalWarewolfPercentage: " << example3.warewolfPercentage << std::endl;
    }

    // Receiving data, altering and sending back 
    if (world_rank == destination){
      // struct type to store the received datatype
      ExampleStruct1 recv_example1;
      
      //receive data
	    MPI_Recv(&recv_example1, 1, mpiHostStruct1,source,0,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
      
      //print struct data
      std::cout<<"ExampleStruct1: "<< std::endl;
      std::cout << "List: " << recv_example1.list[0] <<std::endl;
      std::cout << "List: " << recv_example1.list[1] <<std::endl;
      std::cout << "List: " << recv_example1.list[2] <<std::endl;
      std::cout << "Size: " << recv_example1.size << std::endl;
      std::cout << "Letter: " << recv_example1.letter << std::endl;
      std::cout << "Number: " << recv_example1.number << std::endl;
      std::cout << "X: " << recv_example1.x << std::endl;
      std::cout << "Y: " << recv_example1.y << std::endl;
      
      
      
      //end line to seperate structs
      std::cout<<std::endl;
      
      // struct type to store the received datatype
      ExampleStruct2 recv_example2;
      
      //receive data
	    MPI_Recv(&recv_example2, 1, mpiHostStruct2,source,0,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
      
      //print struct data
      std::cout<<"ExampleStruct2: "<< std::endl;
      std::cout << "PlayerList: " << recv_example2.playerlist[0] <<std::endl;
      std::cout << "PlayerList: " << recv_example2.playerlist[1] <<std::endl;
      std::cout << "PlayerList: " << recv_example2.playerlist[2] <<std::endl;
      std::cout << "PlayerListSize: " << recv_example2.playerlistSize << std::endl;
      std::cout << "levelName: " << recv_example2.levelName << std::endl;
      std::cout << "RandVar: " << recv_example2.randVar << std::endl;
      std::cout << "GameBoardWidth: " << recv_example2.gameBoardWidth << std::endl;
      std::cout << "GameBoardHeight: " << recv_example2.gameBoardHeight << std::endl;
      
      
      
      //end line to seperate structs
      std::cout<<std::endl;
      
      // struct type to store the received datatype
      ExampleStruct3 recv_example3;
      
      //receive data
	    MPI_Recv(&recv_example3, 1, mpiHostStruct3,source,0,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
         
      //print struct data
      std::cout<<"ExampleStruct3: "<< std::endl;
      std::cout << "PlayerName: " << recv_example3.playerName <<std::endl;
      std::cout << "PlayerNameSize: " << recv_example3.playerNameSize << std::endl;
      std::cout << "PlayerHealth: " << recv_example3.playerHealth << std::endl;
      std::cout << "PlayerMana: " << recv_example3.playerMana << std::endl;
      std::cout << "ItemList: " << recv_example3.itemList << std::endl;
      std::cout << "ItemListSize: " << recv_example3.itemListSize << std::endl;
      std::cout << "WarewolfPercentage: " << recv_example3.warewolfPercentage << std::endl;
      
      //end line to seperate structs
      std::cout<<std::endl;
      
      //change data in struct1
      recv_example1.list[0] = 1.5;
      recv_example1.list[1] = 1.2;
      recv_example1.list[2] = 1.3;
      recv_example1.list[3] = 7.5;
      recv_example1.size = 4;
      recv_example1.letter = 'b';
      recv_example1.number = 73.6;
      recv_example1.x = 8;
      recv_example1.y = 6;
      
      //send them back to the original node
      MPI_Send(&recv_example1,1, mpiHostStruct1, source, 0, MPI_COMM_WORLD);
      
      //change data in struct 2
      recv_example2.playerlist[0] = 4;
      recv_example2.playerlist[1] = 5;
      recv_example2.playerlist[2] = 6;
      recv_example2.playerlist[3] = 7;
      recv_example2.playerlistSize = 4;
      //create a new string for level name
      std::string newLevelName = "arena";
      //loop through the new level name length and set the struct's level name to be the new level name
      for(int i = 0; i<newLevelName.length();i++)
      {
        recv_example2.levelName[i] = newLevelName[i];
      }
      // if the old level name was longer than the new level name
      if(newLevelName.length()<recv_example2.levelNameSize)
      {
        //loop through structs level name starting from where the new level name stopped
        for(int i = newLevelName.length();i<recv_example2.levelNameSize;i++)
        {
          //assign old chars to space char to remove them
          recv_example2.levelName[i] = ' ';
        }
      }
      recv_example2.levelNameSize = 5;
      recv_example2.randVar = 22.3;
      recv_example2.gameBoardWidth = 34;
      recv_example2.gameBoardHeight = 13;
      
      //send them back to the original node
      MPI_Send(&recv_example2,1, mpiHostStruct2, source, 0, MPI_COMM_WORLD);
      
      //change data in struct3
      //create a new string for player name
      std::string newPlayerName = "villain";
      //loop through the new player name length and set the struct's level name to be the new player name
      for(int i = 0; i<newPlayerName.length();i++)
      {
        recv_example3.playerName[i] = newPlayerName[i];
      }
      // if the old player name was longer than the new player name
      if(newPlayerName.length()<recv_example3.playerNameSize)
      {
        //loop through structs player name starting from where the new player name stopped
        for(int i = newPlayerName.length();i<recv_example3.playerNameSize;i++)
        {
          //assign old chars to space char to remove them
          recv_example3.playerName[i] = ' ';
        }
      }
      recv_example3.playerNameSize = 7;
      recv_example3.playerHealth = 231.2;
      recv_example3.playerMana = 105.9;
      //create a new string for player name
      std::string newItemList = "lifesteal";
      //loop through the new item list length and set the struct's item list to be the new item list
      for(int i = 0; i<newItemList.length();i++)
      {
        recv_example3.itemList[i] = newItemList[i];
      }
      // if the old item list was longer than the new item list
      if(newItemList.length()<recv_example3.itemListSize)
      {
        //loop through structs item list starting from where the new item list stopped
        for(int i = newItemList.length();i<recv_example3.itemListSize;i++)
        {
          //assign old chars to space char to remove them
          recv_example3.itemList[i] = ' ';
        }
      }
      recv_example3.itemListSize = 9;
      recv_example3.warewolfPercentage = 92.7;
      
      //send them back to the original node	
      MPI_Send(&recv_example3,1, mpiHostStruct3, source, 0, MPI_COMM_WORLD);    
	}


    MPI_Finalize();
    return 0;
}