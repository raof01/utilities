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

    template <typename T>
    static void AddBegin1Pair(const string &, const pair<string, T> &);
    template <typename T>
    static void AddEnd1Pair(const string&, const pair<string, T>&);
    template <typename T>
    static void AddMsg1Pair(const string&, const pair<string, T>&);

    template <typename T1, typename T2>
    static void AddBegin2Pairs(const string&,
                               const pair<string, T1>&,
                               const pair<string, T2>&);
    template <typename T1, typename T2>
    static void AddEnd2Pairs(const string&,
                             const pair<string, T1>&,
                             const pair<string, T2>&);
    template <typename T1, typename T2>
    static void AddMsg2Pairs(const string&,
                             const pair<string, T1>&,
                             const pair<string, T2>&);

    template <typename T1, typename T2, typename T3>
    static void AddBegin3Pairs(const string&,
                               const pair<string, T1>&,
                               const pair<string, T2>&,
                               const pair<string, T3>&);
    template <typename T1, typename T2, typename T3>
    static void AddEnd3Pairs(const string&,
                             const pair<string, T1>&,
                             const pair<string, T2>&,
                             const pair<string, T3>&);
    template <typename T1, typename T2, typename T3>
    static void AddMsg3Pairs(const string&,
                             const pair<string, T1>&,
                             const pair<string, T2>&,
                             const pair<string, T3>&);
private:
    static ostream& AddTagToOstream(ostream&, const string&, const string&);
    static ostream& AddMsgToOstream(ostream&, const string&);

private:
    static MyTime mTime;
};
}
#include "Logger.incl"

#endif
