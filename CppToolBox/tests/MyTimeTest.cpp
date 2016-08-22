#include "gtest/gtest.h"
#include "MyTime.h"
#include <thread>
#include <chrono>

TEST(MyTime, GetMilliSecondsPassed)
{
    MyTime myTimeNow = MyTime();
    std::this_thread::sleep_for(std::chrono::seconds(1));
    ASSERT_EQ(1, static_cast<int>(myTimeNow.GetMilliSecondsPassed() / 1000));
}
