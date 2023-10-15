#ifndef FOREST_H
#define FOREST_H

#include <array>

#define N_FEATURES 3000 //00
#define N_TREES 50

int predict(const std::array<double, N_FEATURES>& features);

#endif // FOREST_H
