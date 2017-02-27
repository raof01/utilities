#ifndef _INI_PARSER_H
#define _INI_PARSER_H

#include <string>
#include <map>
#include <sstream>
#include <vector>

using std::string;
using std::pair;
using std::map;
using std::vector;
using std::istringstream;

/*
 * The ini file format:
 * [SectionName]
 * Key1 = Value1
 * Key2 = Value2
 * ...
 *
 * If there's only one section in ini file, then [section] can be omitted
 */

namespace CppToolBox
{

const string DEFAULT_SECTION = "Default";

class IniParser
{
public:
    IniParser(const string& fName);
    ~IniParser();

public:
    template <typename T>
    T GetValue(const string& name) const
    {
        T v = T();
        istringstream(FindByKey(name)) >> v;
        return v;
    }

    template <typename T>
    T GetValue(const string& secName, const string& keyName) const
    {
        T v = T();
        istringstream(FindByKeyInSection(secName, keyName)) >> v;
        return v;
    }

    template <typename T>
    void AllValues(vector<T>& v) const
    {
        vector<string> sv;
        AllValues(sv);
        StringsToValues(sv, v);
    }

    template <typename T>
    void AllValues(const string& sectName, vector<T>& v) const
    {
        vector<string> sv;
        AllValues(sectName, sv);
        StringsToValues(sv, v);
    }

public:
    bool HasSection(const string& sectionName) const;
    bool HasKey(const string& keyName) const;
    bool HasKey(const string& secName, const string& keyName) const;
    int SectionCount() const;
    // Section names can not duplicate but can have same pattern
    int SectionCount(const string& secNamePattern) const;
    int KeyValueCount(const string& sectionName) const;
    int KeyValueCount() const;
    void AllValues(vector<string>& v) const;
    void AllValues(const string& s, vector<string>& v) const;

    bool Parse();

private:
    string FindByKey(const string& k) const;
    string FindByKeyInSection(const string& s, const string& k) const;

    template <typename T>
    void StringsToValues(const vector<string>& sv, vector<T>& vv) const
    {
        vv.clear();
        for(auto iter = std::begin(sv);
            iter != std::end(sv); ++iter)
        {
            T val;
            istringstream(*iter) >> val;
            vv.push_back(val);
        }
    }

private:
    typedef map<string, string> SectionType;
    typedef map<string, SectionType> IniTreeType;

private:
    /*
     * pair<sectionName, pair<keyName, value>>
     * Empty sectionName means no section.
     */
    string mIniFileName;
    IniTreeType mKeyValues;
};

}

#endif
