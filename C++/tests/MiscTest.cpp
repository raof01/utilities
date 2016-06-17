#include "gtest/gtest.h"
#include <sstream>

TEST(MiscTest, TestNumToString)
{
    std::ostringstream oss;
    oss << "Hello" << 10;
    ASSERT_EQ(0, oss.str().compare(("Hello10")));
}
