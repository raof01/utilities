#include <fstream>
#include <sstream>
#include <algorithm>
#include <functional>
#include <cctype>
#include <locale>
#include "IniParser.h"

using std::ifstream;
using std::istringstream;
using std::ptr_fun;
using std::not1;
using std::isspace;

const string OPEN_BRACKET = "[";
const string CLOSE_BRACKET = "]";
const string EQUAL_SIGN = "=";
const string COMMENT_SIGN = "#";

using CppToolBox::IniParser;

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
    return s.substr(1, s.length() - 2);
}

// trim from start
static inline string &LeftTrim(string &s)
{
    s.erase(s.begin(), find_if(s.begin(), s.end(), not1(ptr_fun<int, int>(isspace))));
    return s;
}

// trim from end
static inline string &RightTrim(string &s)
{
    s.erase(find_if(s.rbegin(), s.rend(), not1(ptr_fun<int, int>(isspace))).base(), s.end());
    return s;
}

// trim from both ends
static inline string &Trim(string &s)
{
    return LeftTrim(RightTrim(s));
}

static bool IsConfiguration(const string& s)
{
    return s.find(EQUAL_SIGN) != string::npos;
}

static string GetValidSection(const string& s)
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

static string RemoveComment(const string& s)
{
    string::size_type p = s.find(COMMENT_SIGN);
    if (p != string::npos)
        return s.substr(0, p);
    return s;
}

bool IniParser::Parse()
{
    ifstream iniFile(mIniFileName);
    if (!iniFile.good()) return false;
    string line;
    string savedSecName;
    map<string, string> keyValues;
    while(std::getline(iniFile, line))
    {
        line = RemoveComment(line);
        Trim(line);
        string secName;
        if (!IsConfiguration(line))
        {
          secName = GetValidSection(line);
          if (secName.empty()) continue;
          if (secName.compare(savedSecName) != 0)
          {
              // New section, but not first section
              if (!savedSecName.empty())
                  mKeyValues.insert(make_pair(savedSecName, keyValues));
              keyValues.clear();
              savedSecName = secName;
          }
        }
        else
        {
            if (savedSecName.empty()) savedSecName = DEFAULT_SECTION;
            istringstream iss(line);
            string key, equal, value;
            iss >> key >> equal >> value;
            keyValues.insert(make_pair(key, value));
        }
    }
    // The last section should be saved
    if (!savedSecName.empty())
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

string IniParser::FindByKeyInSection(const string &s, const string &k) const
{
    if (s.empty()) return FindByKey(k);
    SectionType::const_iterator i = mKeyValues.find(s)->second.find(k);
    return i->second;
}

bool IniParser::HasSection(const string &sectionName) const
{
    return mKeyValues.find(sectionName) != mKeyValues.end();
}

bool IniParser::HasKey(const string &keyName) const
{
    for (IniTreeType::const_iterator iter = mKeyValues.begin();
         iter != mKeyValues.end(); ++iter)
    {
        if (iter->second.find(keyName) != iter->second.end())
            return true;
    }
    return false;
}

bool IniParser::HasKey(const string &secName, const string &keyName) const
{
    IniTreeType::const_iterator secIter = mKeyValues.find(secName);
    return secIter == mKeyValues.end() ? false : secIter->second.find(keyName) != secIter->second.end();
}

int IniParser::SectionCount() const
{
    return mKeyValues.size();
}

int IniParser::SectionCount(const string &secNamePattern) const
{
    int cnt = 0;
    for (IniTreeType::const_iterator iter = mKeyValues.begin();
         iter != mKeyValues.end(); ++iter)
    {
        if (iter->first.find(secNamePattern) != string::npos)
            ++cnt;
    }
    return cnt;
}

int IniParser::KeyValueCount(const string &sectionName) const
{
    if (!HasSection(sectionName)) return 0;
    IniTreeType::const_iterator iter = mKeyValues.find(sectionName);
    return iter->second.size();
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

void IniParser::AllValues(const string &s, vector<string>& v) const
{
    v.clear();
    if (!HasSection(s)) return;
    IniTreeType::const_iterator section = mKeyValues.find(s);
    for (SectionType::const_iterator iter = section->second.begin();
         iter != section->second.end(); ++iter)
    {
        v.push_back(iter->second);
    }
}

void IniParser::AllValues(vector<string>& v) const
{
    v.clear();
    for(IniTreeType::const_iterator iter = mKeyValues.begin();
        iter != mKeyValues.end(); ++iter)
    {
        for (SectionType::const_iterator sIter = iter->second.begin();
             sIter != iter->second.end(); ++sIter)
            v.push_back(sIter->second);
    }
}
