// #include <stdlib.h>
// #include <stdio.h>
#include <iostream>
#include <math.h>
#include <vector>
#include <array>
#include <map>

#include "children_left.h"
#include "children_right.h"
#include "feature.h"
#include "threshold.h"
#include "value.h"

#define N_FEATURES 3000
#define N_TREES 50


int predictTree(const std::array<double, N_FEATURES>& features, int node, int tree) {
    while (allThresholds[tree][node] != -2) {
        if (features[allIndices[tree][node]] <= allThresholds[tree][node]) {
            node = allLeftChildren[tree][node];
        } else {
            node = allRightChildren[tree][node];
       }
    }
    return allClasses[tree][node];
}

int predict(const std::array<double, N_FEATURES>& features) {
    std::map<int, int> predictionsFrequency;
    
    for (int tree = 0; tree < N_TREES; ++tree) {
        int prediction = predictTree(features, 0, tree);
        std::cout << tree << std::endl;
        predictionsFrequency[prediction]++;
    }
    
    int maxFrequency = -1;
    int mostFrequentPrediction = -1;
    
    for (const auto& pair : predictionsFrequency) {
        if (pair.second > maxFrequency) {
            maxFrequency = pair.second;
            mostFrequentPrediction = pair.first;
        }
    }
    
    return mostFrequentPrediction;
}

int main() {
    std::array<double, N_FEATURES> features{};
    std::cout << "start" << std::endl;
    for (int i = 0; i < N_FEATURES; i++)
        features[i] = 0.1;
    std::cout << predict(features) << std::endl;
    return 0;

}
