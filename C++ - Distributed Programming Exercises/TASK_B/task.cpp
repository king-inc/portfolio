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
	}


    MPI_Finalize();
    return 0;
}