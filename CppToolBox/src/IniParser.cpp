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
using std::begin;
using std::end;
using std::rbegin;
using std::rend;

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
    s.erase(begin(s), find_if(begin(s), end(s), not1(ptr_fun<int, int>(isspace))));
    return s;
}

// trim from end
static inline string &RightTrim(string &s)
{
    s.erase(find_if(rbegin(s), rend(s), not1(ptr_fun<int, int>(isspace))).base(), s.end());
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
    auto name = GetSectionName(s);
    if (name.find(OPEN_BRACKET) != string::npos || name.find(CLOSE_BRACKET) != string::npos)
        return string();
    return name;
}

static string RemoveComment(const string& s)
{
    auto p = s.find(COMMENT_SIGN);
    if (p != string::npos)
        return s.substr(0, p);
    return s;
}

bool IniParser::Parse()
{
    auto iniFile = ifstream(mIniFileName);
    if (!iniFile.good()) return false;
    auto line = string();
    auto savedSecName = string();
    map<string, string> keyValues;
    while(std::getline(iniFile, line))
    {
        line = RemoveComment(line);
        Trim(line);
        auto secName = string();
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
            auto iss = istringstream(line);
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
    for (auto iter = begin(mKeyValues);
         iter != end(mKeyValues); ++iter)
    {
        auto i = iter->second.find(k);
        if (i != end(iter->second))
            return i->second;
    }
    return string();
}

string IniParser::FindByKeyInSection(const string &s, const string &k) const
{
    if (s.empty()) return FindByKey(k);
    auto i = mKeyValues.find(s)->second.find(k);
    return i->second;
}

bool IniParser::HasSection(const string &sectionName) const
{
    return mKeyValues.find(sectionName) != end(mKeyValues);
}

bool IniParser::HasKey(const string &keyName) const
{
    for (auto iter = begin(mKeyValues);
         iter != end(mKeyValues); ++iter)
    {
        if (iter->second.find(keyName) != end(iter->second))
            return true;
    }
    return false;
}

bool IniParser::HasKey(const string &secName, const string &keyName) const
{
    auto secIter = mKeyValues.find(secName);
    return secIter == end(mKeyValues) ? false : secIter->second.find(keyName) != end(secIter->second);
}

int IniParser::SectionCount() const
{
    return mKeyValues.size();
}

int IniParser::SectionCount(const string &secNamePattern) const
{
    int cnt = 0;
    for (auto iter = begin(mKeyValues);
         iter != end(mKeyValues); ++iter)
    {
        if (iter->first.find(secNamePattern) != string::npos)
            ++cnt;
    }
    return cnt;
}

int IniParser::KeyValueCount(const string &sectionName) const
{
    if (!HasSection(sectionName)) return 0;
    auto iter = mKeyValues.find(sectionName);
    return iter->second.size();
}

int IniParser::KeyValueCount() const
{
    int cnt = 0;
    for (auto iter = begin(mKeyValues);
         iter != end(mKeyValues); ++iter)
    {
        cnt += iter->second.size();
    }
    return cnt;
}

void IniParser::AllValues(const string &s, vector<string>& v) const
{
    v.clear();
    if (!HasSection(s)) return;
    auto section = mKeyValues.find(s);
    for (auto iter = begin(section->second);
         iter != end(section->second); ++iter)
    {
        v.push_back(iter->second);
    }
}

void IniParser::AllValues(vector<string>& v) const
{
    v.clear();
    for(auto iter = begin(mKeyValues);
        iter != end(mKeyValues); ++iter)
    {
        for (auto sIter = begin(iter->second);
             sIter != end(iter->second); ++sIter)
            v.push_back(sIter->second);
    }
}
