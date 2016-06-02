#include "gtest/gtest.h"
#include "iniparser.h"

TEST(IniParser, GetValue_ReturnInt)
{
    IniParser iniParser;
    ASSERT_EQ(0, iniParser.GetValue<int>(string("foo")));
}
