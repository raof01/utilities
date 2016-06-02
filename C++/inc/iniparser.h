#ifndef _INI_PARSER_H
#define _INI_PARSER_H

#include <string>
#include <vector>

using std::string;
using std::vector;
using std::pair;

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
    bool Parse();
    bool Parse(const string& fName);
    template <typename T>
    T GetValue(const string& name) const
    {
        return T();
    }
    bool HasSection(const string& sectionName) const;
    bool HasKey(const string& keyName) const;
    int Sections() const;
    int KeyValues(const string& sectionName) const;
    int KeyValues() const;

private:
    vector<string> mSections;
    vector<pair<string, string>> mKeyValues;
};

#endif
