
#include <utility>
#include "gtest/gtest.h"
#include "Logger.h"

using namespace CppToolBox;
#if VS2013 != 1
TEST(TestLogger, Printing)
{
    Logger::Setup();
    Logger::AddBegin(__FUNCTION__);
    Logger::AddEnd(__FUNCTION__);
    Logger::AddMsg("this is a free message");
    Logger::AddBeginPairs(__FUNCTION__, std::make_pair<string, double>("Key", 0.03));
    Logger::AddEndPairs(__FUNCTION__, std::make_pair<string, double>("Key", 0.03));
    Logger::AddMsgPairs("this is a free message", std::make_pair<string, double>("Key", 0.03));
    Logger::AddBeginPairs(__FUNCTION__,
                           std::make_pair<string, double>("KeyBegin1", 0.02),
                           std::make_pair<string, double>("KeyBegin2", 0.02));
    Logger::AddEndPairs(__FUNCTION__,
                         std::make_pair<string, double>("KeyEnd1", 0.02),
                         std::make_pair<string, double>("KeyEnd2", 0.02));
    Logger::AddMsgPairs(__FUNCTION__,
                         std::make_pair<string, double>("KeyMsg1", 0.02),
                         std::make_pair<string, double>("KeyMsg2", 0.02));
    Logger::AddBeginPairs(__FUNCTION__,
                           std::make_pair<string, double>("KeyBegin1", 0.02),
                           std::make_pair<string, string>("KeyBegin2", "Value1"),
                           std::make_pair<string, string>("KeyBegin3", "Value2"));
    Logger::AddEndPairs(__FUNCTION__,
                         std::make_pair<string, double>("KeyEnd1", 0.02),
                         std::make_pair<string, double>("KeyEnd2", 0.02),
                         std::make_pair<string, string>("KeyEnd3", "Value1"));
    Logger::AddMsgPairs(__FUNCTION__,
                         std::make_pair<string, double>("KeyMsg1", 0.02),
                         std::make_pair<string, double>("KeyMsg2", 0.02),
                         std::make_pair<string, string>("KeyMsg3", "Value1"));
}

#endif
