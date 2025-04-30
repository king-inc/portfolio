#include "omp.h"
#include <iostream>
#include <cmath>
#include <cstdlib>
#include <unistd.h>
#include <chrono>
#include <thread>
#include <time.h>

#define THREADS 4
#define N 20


/*function multiplies each iteration by 5 and outptus the thead number, iteration and result*/
int main ()
{
    //iteration variable
    int i;
    
    #pragma omp parallel for schedule (dynamic), num_threads (THREADS)
    for(i=0; i<=N; i++)
    {
      //result is 5 times the iteration variable
      int result = 5 * i;
      //print the thread number, the current itration and the result 
      std::cout<<"Thread"<<" "<<omp_get_thread_num()<<" "<<"has completed iteration"<<" "<<i<<" "<<"resulting in"<<" "<<result<<std::endl;
    }
    
    //print when all threads finish
    std::cout<<"All threads done"<<std::endl;
    return 0;
}