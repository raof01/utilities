#include "Logger.h"

using std::cerr;
using std::endl;

using CppToolBox::Logger;
using CppToolBox::MyTime;

MyTime Logger::mTime = MyTime();

void Logger::AddBegin(const string & funcName)
{
    AddTagToOstream(cerr, funcName, BEGIN) << endl;
}

void Logger::AddEnd(const string & funcName)
{
    AddTagToOstream(cerr, funcName, END) << endl;
}

void Logger::AddMsg(const string & msg)
{
    AddMsgToOstream(cerr, msg) << endl;
}

void Logger::Setup()
{
    cerr.precision(PRECISION);
    cerr.setf(ios::left);
}

ostream& Logger::AddTagToOstream(ostream& os, const string& f, const string& s)
{
    os << setw(TIMESTAMP_WIDTH)
       << mTime.GetMilliSecondsPassed()
       << MILLI_SECOND << COLON
       << setw(FUNCTION_NAME_WIDTH) << f << COLON
       << setw(STATE_WIDTH) << s;
    return os;
}

ostream& Logger::AddMsgToOstream(ostream& os, const string& msg)
{
    os << setw(TIMESTAMP_WIDTH)
       << mTime.GetMilliSecondsPassed()
       << MILLI_SECOND << COLON << msg;
    return os;
}
