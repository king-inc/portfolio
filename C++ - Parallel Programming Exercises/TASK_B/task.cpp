#include "omp.h"
#include <iostream>
#include <fstream>
#include <cmath>
#include <cstdlib>
#include <unistd.h>
#include <chrono>
#include <thread>
#include <time.h>
#include <vector>
#include "stdio.h"

#define THREADS 4
#define ITERATIONS 50
int main()
{
  //array of vectors
  std::vector<int> V[10] = {{5,14,10},{7,-8,-14},{-2,9,8},{15,-6,3},{12,4,-5},{4,20,17},{-16,5,-1},{-11,3,16},{3,10,-19},{-16,7,4}};
  
  //Particle Position Alteration
  int PPA = 2;
  
  /* original state */  
  std::cout<<"Original State: "<< std::endl;
  for(int i=0; i<10; i++)
  {
    std::cout << "Vector at index "<< i << ": "; 
    //iterate through each vector and print it 
    for(auto it=V[i].begin(); it!=V[i].end(); it++)
    {
      //print vectors
      std::cout << *it <<' ';
    }
    //end line
    std::cout<<std::endl;
  }
  
  #pragma omp parallel for ordered
  for(int k=0; k<ITERATIONS; k++)
  {
    //pragma directive to collapse the two for loops and specify the number of threads used
    #pragma omp parallel for collapse(2), num_threads (THREADS)
      for(int i=0; i<10; i++)
      {
        //iterate through array of vectors 
        for(int j = 0; j< 3; j++)
        {
          //increment or decrement current vector
          //charge gets a random number between 1 and 2  
          int charge = rand() % 2 + 1;
          
          //if charge is 2 then increase vector (charge is +1)
          if(charge>1)
          {
            charge = 1;
          }
          //if charge is 1 then decrease vector (charge is -1)  
          else
          {
            charge = -1;
          }
          
          //multiply the PPA by the charge to reduce or increase the vector positions
          V[i][j] = V[i][j] + (PPA*charge);   
        }
      }
      
    //critical section to prevent race condition to PPA and vector assignment
    #pragma omp critical
    {
      //increase the PPA by a random number between one and five 
      PPA = PPA + (rand() % 5 + 1);
    }
    
    #pragma omp ordered
    //print array of vectors at 25th and 50th iteration
    if(k==24 || k==49)
    {
      //save the results of the text file to be used in task C
      std::ofstream results("resultB.txt");
      std::cout<<k+1 <<"th Iteration State"<< std::endl;
      for(int i=0; i<10; i++)
      {
        //iterate through vector to print and save it
        std::cout << "Vector at index "<< i << ": "; 
        for(auto it=V[i].begin(); it!=V[i].end(); it++)
        {
          std::cout << *it <<' ';
          results<<*it<<std::endl;
        }
        //end line
        std::cout<<std::endl;
      }
      //close file
      results.close();
      
    }
  }
  
  

}
