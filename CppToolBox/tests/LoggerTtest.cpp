
#include <utility>
#include "gtest/gtest.h"
#include "Logger.h"

using namespace CppToolBox;

TEST(TestLogger, Printing)
{
    Logger::Setup();
    Logger::AddBegin(__FUNCTION__);
    Logger::AddEnd(__FUNCTION__);
    Logger::AddMsg("this is a free message");
    Logger::AddBegin1Pair(__FUNCTION__, std::make_pair<string, double>("Key", 0.03));
    Logger::AddEnd1Pair(__FUNCTION__, std::make_pair<string, double>("Key", 0.03));
    Logger::AddMsg1Pair("this is a free message", std::make_pair<string, double>("Key", 0.03));
    Logger::AddBegin2Pairs(__FUNCTION__,
                           std::make_pair<string, double>("KeyBegin1", 0.02),
                           std::make_pair<string, double>("KeyBegin2", 0.02));
    Logger::AddEnd2Pairs(__FUNCTION__,
                         std::make_pair<string, double>("KeyEnd1", 0.02),
                         std::make_pair<string, double>("KeyEnd2", 0.02));
    Logger::AddMsg2Pairs(__FUNCTION__,
                         std::make_pair<string, double>("KeyMsg1", 0.02),
                         std::make_pair<string, double>("KeyMsg2", 0.02));
    Logger::AddBegin3Pairs(__FUNCTION__,
                           std::make_pair<string, double>("KeyBegin1", 0.02),
                           std::make_pair<string, string>("KeyBegin2", "Value1"),
                           std::make_pair<string, string>("KeyBegin3", "Value2"));
    Logger::AddEnd3Pairs(__FUNCTION__,
                         std::make_pair<string, double>("KeyEnd1", 0.02),
                         std::make_pair<string, double>("KeyEnd2", 0.02),
                         std::make_pair<string, string>("KeyEnd3", "Value1"));
    Logger::AddMsg3Pairs(__FUNCTION__,
                         std::make_pair<string, double>("KeyMsg1", 0.02),
                         std::make_pair<string, double>("KeyMsg2", 0.02),
                         std::make_pair<string, string>("KeyMsg3", "Value1"));
}

