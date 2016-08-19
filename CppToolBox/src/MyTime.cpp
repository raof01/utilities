#include "MyTime.h"

using std::chrono::duration;


MyTime::MyTime() : mStart()
{
    mStart = high_resolution_clock::now();
}

double MyTime::GetMilliSecondsPassed() const
{
    return duration<double, std::milli>(high_resolution_clock::now() - mStart).count();
}
