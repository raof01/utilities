#include "MyTime.h"

using std::chrono::duration;

using CppToolBox::MyTime;

MyTime::MyTime() : mStart()
{
    mStart = high_resolution_clock::now();
}

double MyTime::GetMilliSecondsPassed() const
{
    return duration<double, std::milli>(high_resolution_clock::now() - mStart).count();
}
