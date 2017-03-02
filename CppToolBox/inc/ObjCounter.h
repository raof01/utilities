#ifndef _OBJ_COUNTER_H
#define _OBJ_COUNTER_H

#include <atomic>
#include <cstdint>

using std::atomic;
using std::uint64_t;

/**
 * Curiously Recuring Template Pattern
 */

namespace CppToolBox
{

template <typename T>
class ObjCounter
{
public:
    static uint64_t CreationCnt() { return mObjCreationCnt.load(); }
    static uint64_t AliveCnt() { return mObjAliveCnt.load(); }

protected:
    ObjCounter();
    ~ObjCounter();
    ObjCounter(const ObjCounter&);

    static atomic<uint64_t> mObjCreationCnt;
    static atomic<uint64_t> mObjAliveCnt;
};

template <typename T>
atomic<uint64_t> ObjCounter<T>::mObjAliveCnt(0);

template <typename T>
atomic<uint64_t> ObjCounter<T>::mObjCreationCnt(0);

template <typename T>
ObjCounter<T>::ObjCounter()
{
    ++mObjAliveCnt;
    ++mObjCreationCnt;
}

template <typename T>
ObjCounter<T>::~ObjCounter()
{
    --mObjAliveCnt;
}

template <typename T>
ObjCounter<T>::ObjCounter(const ObjCounter&)
{
    ++mObjAliveCnt;
    ++mObjCreationCnt;
}

}

#endif
