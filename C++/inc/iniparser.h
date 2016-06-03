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

class IniParser
{
public:
    IniParser();
    IniParser(const string& fName);
    ~IniParser();

public:
    template <typename T>
    T GetValue(const string& name) const
    {
        T v;
        istringstream(FindByKey(name)) >> v;
        return v;
    }

    template <typename T>
    vector<T> GetAllValuesInSection(const string& sectionName) const
    {
        return vector<T>();
    }

    template <typename T>
    vector<T> GetAllValues(const string& sectionName) const
    {
        return vector<T>();
    }

public:
    bool HasSection(const string& sectionName) const;
    bool HasKey(const string& keyName) const;
    int SectionCount() const;
    int KeyValueCount(const string& sectionName) const;
    int KeyValueCount() const;

    bool Parse();

private:
    string FindByKey(const string& k) const;

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

#endif
