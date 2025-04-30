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
#include <string>


#define THREADS 4
#define ITERATIONS 50

//declare array of vectors
std::vector<int> V[10] = {{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0}};

void readResultB()
{
  //open file
  std::fstream result("../TASK_B/resultB.txt");
  std::string tmp;
  //variables for parsing text file to vectors
  //i is the vector count
  int i = 0;
  //j is the position counter
  int j = 0;
  
  //read file line by line
  while(std::getline(result,tmp))
  {
    //if it reaches the third position of a vector, go to the next vector
    if(j==3)
    {
      j = 0;
      i += 1;
    }
    //if it reaches the last vector then stop reading file
    if (i==10)
    {
      break;
    }
    
    //assign the vector the correct values
    V[i][j] = std::stoi(tmp);
    //increase position counter
    j += 1;
  }
}

std::vector<int> findCentroid()
{
  int x = 0;
  int y = 0;
  int z = 0;
  
  //iterate through the array of vectors
  for (int i = 0; i<10; i++)
  {
  //add each vector position to their corresponding coord names
    x += V[i][0];
    y += V[i][1];
    z += V[i][2];
  }
  
  //divide each position by the number of vectors to get the x y z center of all vectors
  std::vector<int> centroid = {x/10,y/10,z/10};
  
  return centroid; 
}

int calculateDistance(std::vector<int> v, std::vector<int> centroid)
{
  //declare variable dist to store distance from vector v to center
  int dist = 0;
  
  for(int i=0; i<3; i++)
  {
    dist += pow((v[i]-centroid[i]),2);
  }
  
  dist = sqrt(dist);
  return dist;
}
  
int main()
{
  //Particle Position Alteration
  int PPA = 2;
  
  //reads in the results of task B stored in a text file
  readResultB();
  //finds the center of all vectors
  std::vector<int> centroid = findCentroid();
  
  //print center of all vectors
  std::cout<<"Center of all Vectors: ";
  for(int i=0;i<3;i++)
  {
    std::cout<<centroid[i] << ' ';
  }
  
  //double end lines to make output look pretty
  std::cout<<std::endl;
  std::cout<<std::endl;
  
  /* original state */  
  std::cout<<"Original State: "<< std::endl;
  for(int i=0; i<10; i++)
  {
    //iterate through each vector and print it 
    std::cout << "Vector at index "<< i << ": "; 
    for(auto it=V[i].begin(); it!=V[i].end(); it++)
    {
      //print vectors
      std::cout << *it <<' ';
    }
    //end line
    std::cout<<std::endl;
    //print distance of each vector from the center
    std::cout <<"Distance from Center: "<< calculateDistance(V[i],centroid)<<std::endl;
  }
  //second end line to make output look pretty
  std::cout<<std::endl;
  
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
          //increment or decrement current vector depending on how far it is from center
          //charge starts with 0
          //this means if the vector position is at the center it does not move
          int charge = 0;
          
          //if the vector position minus the center of vectors is negative
          //which means if the  vector is behind the center, we increase the vector position 
          if(V[i][j]-centroid[j] < 0)
          {
            //make the charge positive
            charge = 1;
          }
          //if the vector position minus the center of vectors is positive
          //which means if the  vector is in front the center vector, we reduce the vector position
          else
          {
          //make the charge negative
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
    //print array of vectors at 13th,25th,37th and 50th iteration
    if( k==12 || k==24 || k==36 || k==49 )
    {
      //print vectors at 25th and 50th iteration
      std::cout<<k+1 <<"th Iteration State"<< std::endl;
      for(int i=0; i<10; i++)
      {
        //iterate through vector to print it
        std::cout << "Vector at index "<< i << ": "; 
        for(auto it=V[i].begin(); it!=V[i].end(); it++)
        {
          std::cout << *it <<' ';
        }
        //end line
        std::cout<<std::endl;
        //print distance of each vector from the center
        std::cout <<"Distance from Center: "<< calculateDistance(V[i],centroid)<<std::endl;
      }
      //second end line to make output look pretty
      std::cout<<std::endl;
      
    }
  }
  
  
}



