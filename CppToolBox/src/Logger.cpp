#include "Logger.h"

using std::cerr;
using std::endl;

using CppToolBox::Logger;
using CppToolBox::MyTime;

ostream& Logger::output(cerr);
MyTime Logger::mTime = MyTime();

void Logger::AddBegin(const string & funcName)
{
    AddTagToOstream(output, funcName, BEGIN) << endl;
}

void Logger::AddEnd(const string & funcName)
{
    AddTagToOstream(output, funcName, END) << endl;
}

void Logger::AddMsg(const string & msg)
{
    AddMsgToOstream(output, msg) << endl;
}

void Logger::Setup()
{
    output.precision(PRECISION);
    output.setf(ios::left);
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
