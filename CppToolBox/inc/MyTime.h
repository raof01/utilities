#ifndef _MY_TIME_H
#define _MY_TIME_H

#include <chrono>

using std::chrono::high_resolution_clock;

class MyTime
{
public:
    MyTime();
    double GetMilliSecondsPassed() const;

private:
    high_resolution_clock::time_point mStart;
};

#endif
