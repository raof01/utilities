#include "gtest/gtest.h"
#include "IniParser.h"

TEST(IniParser, Parse_ReturnFalseWhenIniFileDoesNotExist)
{
    IniParser iniParser("NOSUCHFILE");
    ASSERT_FALSE(iniParser.Parse());
}

TEST(IniParser, Parser_ReturnTrueWhenIniFileExists)
{
    IniParser iniParser("./empty.ini");
    ASSERT_TRUE(iniParser.Parse());
}

TEST(IniParser, Parse_WhenNoSectionPresent)
{
    IniParser iniParser("./no_section.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_EQ(2, iniParser.KeyValueCount());
    ASSERT_DOUBLE_EQ(3.1415926535, iniParser.GetValue<double>("Pi"));
    ASSERT_EQ(0, string("Value1").compare(iniParser.GetValue<string>("Key1")));
}

TEST(IniParser, SectionCount_ReturnOneWhenNoSectionPresent)
{
    IniParser iniParser("./no_section.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_EQ(1, iniParser.SectionCount());
}

TEST(IniParser, SectionCount_ReturnOneWhenOneSectionPresent)
{
    IniParser iniParser("./one_section_no_keyvalue.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_EQ(1, iniParser.SectionCount());
}

TEST(IniParser, SectionCount_ReturnTwoWhenTwoSectionsPresent)
{
    IniParser iniParser("./two_sections_no_keyvalue.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_EQ(2, iniParser.SectionCount());
}

TEST(IniParser, HasSection_ReturnTrueWhenSectionExists)
{
    IniParser iniParser("./two_sections_no_keyvalue.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_TRUE(iniParser.HasSection("Section1"));
    ASSERT_TRUE(iniParser.HasSection("Section2"));
}

TEST(IniParser, HasSection_ReturnTrueWhenNoSection)
{
    IniParser iniParser("./no_section.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_TRUE(iniParser.HasSection(DEFAULT_SECTION));
}

TEST(IniParser, KeyValueCount_ReturnZeorWhenNoKeyValue)
{
    IniParser iniParser("./two_sections_no_keyvalue.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_EQ(0, iniParser.KeyValueCount("Section1"));
    ASSERT_EQ(0, iniParser.KeyValueCount("Section2"));
}


TEST(IniParser, KeyValueCount_ReturnExpectedCountWhenKeyValueExists)
{
    IniParser iniParser("./two_sections.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_EQ(2, iniParser.KeyValueCount("Section1"));
    ASSERT_EQ(2, iniParser.KeyValueCount("Section2"));
    ASSERT_EQ(4, iniParser.KeyValueCount());
}

TEST(IniParser, KeyValueCount_ReturnTrueWhenKeyValueExists)
{
    IniParser iniParser("./two_sections.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_TRUE(iniParser.HasKey("Key1"));
    ASSERT_TRUE(iniParser.HasKey("Key2"));
    ASSERT_TRUE(iniParser.HasKey("Pi"));

    ASSERT_TRUE(iniParser.HasKey("Section1", "Key1"));
    ASSERT_TRUE(iniParser.HasKey("Section1", "Key2"));
    ASSERT_TRUE(iniParser.HasKey("Section2", "Key1"));
    ASSERT_TRUE(iniParser.HasKey("Section2", "Pi"));

    ASSERT_EQ(4, iniParser.KeyValueCount());
}

TEST(IniParser, GetValue_ReturnExpectedValue)
{
    IniParser iniParser("./two_sections.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_EQ(0, iniParser.GetValue<string>("Key1").compare("Value1"));
    ASSERT_EQ(0, iniParser.GetValue<string>("Key2").compare("Value2"));
    ASSERT_DOUBLE_EQ(3.1415926535897, iniParser.GetValue<double>("Pi"));

    ASSERT_EQ(0, iniParser.GetValue<string>("Section1", "Key1").compare("Value1"));
    ASSERT_EQ(0, iniParser.GetValue<string>("Section1", "Key2").compare("Value2"));
    ASSERT_EQ(0, iniParser.GetValue<string>("Section2", "Key1").compare("Value1InSection2"));
    ASSERT_DOUBLE_EQ(3.1415926535897, iniParser.GetValue<double>("Pi"));

    ASSERT_EQ(4, iniParser.KeyValueCount());
}

TEST(IniParser, SectionCount_ReturnExpectedValueWhenLastSectionIsEmpty)
{
    IniParser iniParser("./three_sections_last_empty.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_EQ(3, iniParser.SectionCount());
    ASSERT_EQ(0, iniParser.KeyValueCount("Section3"));

    ASSERT_EQ(4, iniParser.KeyValueCount());
}

TEST(IniParser, GetValue_ReturnExpectedValueWhenLastSectionIsEmpty)
{
    IniParser iniParser("./three_sections_last_empty.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_EQ(0, iniParser.GetValue<string>("Key1").compare("Value1"));
    ASSERT_EQ(0, iniParser.GetValue<string>("Key2").compare("Value2"));
    ASSERT_DOUBLE_EQ(3.1415926535897, iniParser.GetValue<double>("Pi"));

    ASSERT_EQ(0, iniParser.GetValue<string>("Section1", "Key1").compare("Value1"));
    ASSERT_EQ(0, iniParser.GetValue<string>("Section1", "Key2").compare("Value2"));
    ASSERT_EQ(0, iniParser.GetValue<string>("Section2", "Key1").compare("Value1InSection2"));
    ASSERT_DOUBLE_EQ(3.1415926535897, iniParser.GetValue<double>("Pi"));
}

TEST(IniParser, SectionCount_ReturnExpectedValueWhenFirstSectionIsEmpty)
{
    IniParser iniParser("./three_sections_first_empty.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_EQ(3, iniParser.SectionCount());
    ASSERT_EQ(0, iniParser.KeyValueCount("Section3"));
    ASSERT_EQ(4, iniParser.KeyValueCount());
}

TEST(IniParser, GetValue_ReturnExpectedValueWhenFirstSectionIsEmpty)
{
    IniParser iniParser("./three_sections_first_empty.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_EQ(0, iniParser.GetValue<string>("Key1").compare("Value1"));
    ASSERT_EQ(0, iniParser.GetValue<string>("Key2").compare("Value2"));
    ASSERT_DOUBLE_EQ(3.1415926535897, iniParser.GetValue<double>("Pi"));

    ASSERT_EQ(0, iniParser.GetValue<string>("Section1", "Key1").compare("Value1"));
    ASSERT_EQ(0, iniParser.GetValue<string>("Section1", "Key2").compare("Value2"));
    ASSERT_EQ(0, iniParser.GetValue<string>("Section2", "Key1").compare("Value1InSection2"));
    ASSERT_DOUBLE_EQ(3.1415926535897, iniParser.GetValue<double>("Pi"));
}

TEST(IniParser, SectionCount_ReturnExpectedValueWhenSecondSectionIsEmpty)
{
    IniParser iniParser("./three_sections_second_empty.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_EQ(3, iniParser.SectionCount());
    ASSERT_EQ(0, iniParser.KeyValueCount("Section3"));
    ASSERT_EQ(4, iniParser.KeyValueCount());
}

TEST(IniParser, GetValue_ReturnExpectedValueWhenSecondSectionIsEmpty)
{
    IniParser iniParser("./three_sections_second_empty.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_EQ(0, iniParser.GetValue<string>("Key1").compare("Value1"));
    ASSERT_EQ(0, iniParser.GetValue<string>("Key2").compare("Value2"));
    ASSERT_DOUBLE_EQ(3.1415926535897, iniParser.GetValue<double>("Pi"));

    ASSERT_EQ(0, iniParser.GetValue<string>("Section1", "Key1").compare("Value1"));
    ASSERT_EQ(0, iniParser.GetValue<string>("Section1", "Key2").compare("Value2"));
    ASSERT_EQ(0, iniParser.GetValue<string>("Section2", "Key1").compare("Value1InSection2"));
    ASSERT_DOUBLE_EQ(3.1415926535897, iniParser.GetValue<double>("Pi"));
}

TEST(IniParser, GetValue_ReturnExpectedValueWhenAllKeyAreTheSame)
{
    IniParser iniParser("./dup.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_EQ(1, iniParser.GetValue<int>("A"));
    ASSERT_EQ(1, iniParser.KeyValueCount());
}

TEST(IniParser, AllValues_ReturnEmptyVectorForEmptyIni)
{
    IniParser iniParser("./empty.ini");
    ASSERT_TRUE(iniParser.Parse());
    vector<int> v;
    iniParser.AllValues(v);
    ASSERT_TRUE(v.empty());
    iniParser.AllValues("NoSection", v);
    ASSERT_TRUE(v.empty());
}

TEST(IniParser, AllValues_ReturnExpectedVector)
{
    IniParser iniParser("./same_type_value.ini");
    ASSERT_TRUE(iniParser.Parse());
    vector<int> v;
    iniParser.AllValues(v);
    ASSERT_EQ(10, v.size());
    for(int i = 10, j = 0; i > 0 && j < 10; --i, ++j)
        ASSERT_EQ(i, v[j]);
    iniParser.AllValues("Section2", v);
    ASSERT_EQ(4, v.size());
    for(int i = 6, j = 0; i > 2 && j < 4; --i, ++j)
        ASSERT_EQ(i, v[j]);
}

TEST(IniParser, Parser_ReturnNoSectionWhenOnlyCommentContained)
{
    IniParser iniParser("./empty.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_EQ(0, iniParser.KeyValueCount());
}


TEST(IniParser, GetValue_ReturnExpectedValueInNoNameSection)
{
    IniParser iniParser("./one_section_with_no_name_section.ini");
    ASSERT_TRUE(iniParser.Parse());
    ASSERT_EQ(4, iniParser.KeyValueCount());
}
