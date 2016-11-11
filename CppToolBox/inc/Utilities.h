#ifndef _UTILITIES_H
#define _UTILITIES_H

#include <cstdint>

namespace CppToolBox
{

class Utilities
{
public:
    static float Uint32ToFloat(std::uint32_t);
    static std::uint32_t FloatToUint32(float);
};
}

#endif
