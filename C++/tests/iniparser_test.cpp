#include "gtest/gtest.h"
#include "iniparser.h"

TEST(IniParser, Parse_ReturnFalseWhenIniFileDoesNotExist)
{
    IniParser iniParser("NOSUCHFILE");
    ASSERT_FALSE(iniParser.Parse());
}

TEST(IniParser, Parse_WhenNoSectionPresent)
{
    IniParser iniParser("./no_section.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_EQ(2, iniParser.KeyValueCount());
    ASSERT_DOUBLE_EQ(3.1415926535, iniParser.GetValue<double>("Pi"));
}
