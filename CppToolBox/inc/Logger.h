#ifndef __LOGGER_H
#define __LOGGER_H

#include <string>
#include <ostream>
#include "MyTime.h"

using std::string;
using std::pair;
using std::ostream;

namespace CppToolBox
{
#if VS2013 != 1
const int PRECISION = 16;
const int FUNCTION_NAME_WIDTH = 20;
const int KEY_WIDTH = 10;
const int VALUE_WIDTH = 18;
const int TIMESTAMP_WIDTH = 20;
const int STATE_WIDTH = 5;

const string MILLI_SECOND = "(ms)";
const string COLON = ": ";
const string EQ = " = ";
const string BEGIN = "Begin";
const string END = "End";

class Logger
{
public:
    static void Setup();

    static void AddBegin(const string&);
    static void AddEnd(const string&);
    static void AddMsg(const string&);

    template <typename... Ts>
    static void AddBeginPairs(const string&, const pair<string, Ts>&... args);

    template <typename... Ts>
    static void AddEndPairs(const string&, const pair<string, Ts>&... args);

    template <typename... Ts>
    static void AddMsgPairs(const string&, const pair<string, Ts>&... args);

private:
    template <typename T>
    static void AddPairs(const pair<string, T>&);

    template <typename T, typename... Ts>
    static void AddPairs(const pair<string, T>& arg,
                         const pair<string, Ts>&... args);

private:
    static ostream& AddTagToOstream(ostream&, const string&, const string&);
    static ostream& AddMsgToOstream(ostream&, const string&);

private:
    static ostream& output;
    static MyTime mTime;
};
#endif
}
#include "Logger.incl"
#endif

