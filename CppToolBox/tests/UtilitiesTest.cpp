#include "gtest/gtest.h"
#include "Utilities.h"
#include <iostream>

using std::cout;
using std::endl;
using CppToolBox::Utilities;

TEST(UtilitiesTest, TestUint32ToFloat)
{
    ASSERT_FLOAT_EQ(3.1415926535, Utilities::Uint32ToFloat(1078530011));
}

TEST(UtilitiesTest, TestFloatToUint32)
{
    ASSERT_EQ(1078530011, Utilities::FloatToUint32(3.1415926535));
}
