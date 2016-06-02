#include "iniparser.h"

IniParser::IniParser()
    : mSections()
    , mKeyValues()
{
}

IniParser::IniParser(const string &fName)
{

}

IniParser::~IniParser()
{
}

bool IniParser::Parse()
{
    return false;
}

bool IniParser::Parse(const string &fName)
{
    return false;
}

bool IniParser::HasSection(const string &sectionName) const
{
    return false;
}

bool IniParser::HasKey(const string &keyName) const
{
    return false;
}
