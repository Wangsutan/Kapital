/* C++：马克思经济学两大部类简单再生产均衡条件的判断*/

#include <array>
#include <iostream>

bool checkSimpleEquilibrium(const std::array<double, 3> &department1,
                            const std::array<double, 3> &department2) {
  return (department1.at(1) + department1.at(2) == department2.at(0)) ? true
                                                                      : false;
}

int main() {
  std::array departmentOne{4000.00, 1000.00, 1000.00};
  std::array departmentTwo{2000.00, 500.00, 500.00};

  bool ifSimpleEquilibrium =
      checkSimpleEquilibrium(departmentOne, departmentTwo);
  std::cout << "Equilibrium of simple reproduction:\n"
            << std::boolalpha << ifSimpleEquilibrium << '\n';
  return 0;
}
