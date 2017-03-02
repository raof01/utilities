#ifndef _FACTORY_METHOD_H
#define _FACTORY_METHOD_H

#if VS2013 != 1
#include <memory>
#include <mutex>

using std::unique_ptr;
using std::make_unique;
using std::mutex;
using std::lock_guard;

namespace CppToolBox
{

template <typename T>//, typename... Ts>
class FactoryMethod
{
public:
    static unique_ptr<T> GetInstance();

protected:
    FactoryMethod();
    ~FactoryMethod();
    static unique_ptr<T> mInstance;

private:
    static mutex mLock;
};

template <typename T>
unique_ptr<T> FactoryMethod<T>::GetInstance()
{
    lock_guard<mutex> lock(mLock);
    if (mInstance == nullptr)
        mInstance = make_unique<T>();//std::forward(Ts)...);
    return std::move(mInstance);
}

}

#endif
#endif
