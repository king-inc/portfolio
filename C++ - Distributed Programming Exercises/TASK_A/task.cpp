
#include <iostream>
#include "mpi.h"
#include <cstdlib>
#include <string>

std::string run_command(const char* command)
{
  FILE *fp = popen(command, "r");
    std::string out;
    char buf[1024]; 
    while (fgets(buf, sizeof(buf), fp) != NULL) { 
        //printf("%s", buf);
        out += buf; 
    } 
    pclose(fp); 
    return out;
}

int main(int argc, char** argv) {

  // Initialize the MPI environment
  MPI_Init(NULL, NULL);
  char node_name[MPI_MAX_PROCESSOR_NAME];
  int rank,size, namelen;
  //int num_cores = system("nproc");
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);
  MPI_Get_processor_name(node_name, &namelen);
  std::string num_cores = run_command("nproc");
  std::string clock_speed = run_command("cat /proc/cpuinfo | grep GHz | awk 'NR==1{print $9}'");
  std::string ram = run_command("grep MemTotal /proc/meminfo | awk 'NR==1{print $2,$3}'");
  std::string hostname = run_command("hostname");
  
  std::cout << "-----------------------"<<std::endl;
  std::cout<<"Rank: "<< rank<<", Size: " <<size<<std::endl;
  std::cout<<"Node name: " <<node_name<<std::endl;
  std::cout<<"Number of Cores: " <<num_cores<<std::endl;
  std::cout<<"Clock Speed of Cores: " <<clock_speed<<std::endl;
  std::cout<<"RAM: " <<ram<<std::endl;
  std::cout<<"HOST NAME: " <<hostname<<std::endl;
  
  
  
  MPI_Finalize();
}


