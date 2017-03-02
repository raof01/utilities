#include "gtest/gtest.h"
#include "ObjCounter.h"

using CppToolBox::ObjCounter;

/**
 * @brief usage of ObjCounter
 */

class MyObj: public ObjCounter<MyObj>
{
public:
    MyObj(): ObjCounter<MyObj>() {}
    ~MyObj() {}
    MyObj(const MyObj& m): ObjCounter<MyObj>(m) {}
};

TEST(ObjCounter, SampleUsage)
{
    auto m = MyObj();
    ASSERT_EQ(1, m.CreationCnt());
    ASSERT_EQ(1, m.AliveCnt());
    {
        auto m1(m);
        ASSERT_EQ(2, m1.CreationCnt());
        ASSERT_EQ(2, m1.AliveCnt());
    }
    ASSERT_EQ(1, m.AliveCnt());
    ASSERT_EQ(2, m.CreationCnt());
}
