#include "Utilities.h"

using CppToolBox::Utilities;

union ConvertFloat
{
    std::uint32_t mInt;
    float mFloat;
};

// Simple implementation
float Utilities::Uint32ToFloat(std::uint32_t i)
{
    ConvertFloat c;
    c.mInt = i;
    return c.mFloat;
}

std::uint32_t Utilities::FloatToUint32(float f)
{
    ConvertFloat c;
    c.mFloat = f;
    return c.mInt;
}

