#include <fstream>
#include <sstream>
#include "iniparser.h"

using std::ifstream;
using std::istringstream;

const string OPEN_BRACKET = "[";
const string CLOSE_BRACKET = "]";
const string EQUAL_SIGN = "=";

IniParser::IniParser()
    : mIniFileName()
    , mKeyValues()
{
}

IniParser::IniParser(const string &fName)
    : mIniFileName(fName)
    , mKeyValues()
{
}

IniParser::~IniParser()
{
}

string GetSectionName(const string& s)
{
    return s.substr(1, s.length() - 1);
}

bool IsConfiguration(const string& s)
{
    return s.find(EQUAL_SIGN) != string::npos;
}

string GetValidSection(const string& s)
{
    if (s.length() == 2)
        return string();
    if (s.find(OPEN_BRACKET) != 0 || s.find(CLOSE_BRACKET) != s.length() - 1)
        return string();
    string name = GetSectionName(s);
    if (name.find(OPEN_BRACKET) != string::npos || name.find(CLOSE_BRACKET) != string::npos)
        return string();
    return name;
}

bool IniParser::Parse()
{
    ifstream iniFile = ifstream(mIniFileName);
    if (!iniFile.good()) return false;
    string line;
    string savedSecName;
    map<string, string> keyValues;
    while(std::getline(iniFile, line))
    {
        string secName;
        if (!IsConfiguration(line))
        {
          secName = GetValidSection(line);
          if (secName.compare(savedSecName) != 0)
          {
              if (!keyValues.empty())
                  mKeyValues.insert(make_pair(savedSecName, keyValues));
              keyValues.clear();
              savedSecName = secName;
          }
        }
        else
        {
            istringstream iss(line);
            string key, equal, value;
            iss >> key >> equal >> value;
            keyValues.insert(make_pair(key, value));
        }
    }
    if (!keyValues.empty())
        mKeyValues.insert(make_pair(savedSecName, keyValues));
    return true;
}

string IniParser::FindByKey(const string &k) const
{
    for (IniTreeType::const_iterator iter = mKeyValues.begin();
         iter != mKeyValues.end(); ++iter)
    {
        SectionType::const_iterator i = iter->second.find(k);
        if (i != iter->second.end())
            return i->second;
    }
    return string();
}

bool IniParser::HasSection(const string &sectionName) const
{
    return false;
}

bool IniParser::HasKey(const string &keyName) const
{
    return false;
}

int IniParser::SectionCount() const
{
    return -1;
}

int IniParser::KeyValueCount(const string &sectionName) const
{
    return -1;
}

int IniParser::KeyValueCount() const
{
    int cnt = 0;
    for (IniTreeType::const_iterator iter = mKeyValues.begin();
         iter != mKeyValues.end(); ++iter)
    {
        cnt += iter->second.size();
    }
    return cnt;
}
