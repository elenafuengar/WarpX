#include <PlasmaInjector.H>

#include <iostream>

Real CustomPlasmaInjector::getDensity(Real x, Real y, Real z) {
  std::cout << "Using custom getDensity" << std::endl;
  return 0.0;
}
