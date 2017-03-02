#include "gtest/gtest.h"
#include "FactoryMethod.h"
#if VS2013 != 1
using CppToolBox::FactoryMethod;

/**
 * @brief TEST
 */

class MyObj : public FactoryMethod<MyObj>
{
    friend class FactoryMethod<MyObj>;
private:
    MyObj();

public:
    int mVal;
};

MyObj::MyObj() = default;

TEST(FactoryMethod, SampleUsage)
{
    auto f = MyObj::GetInstance();
    ASSERT_EQ(0, f->mVal);
}
#endif
