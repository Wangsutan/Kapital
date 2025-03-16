#include <array>
#include <iostream>

int main() {
  std::array departmentOne{4000.00, 1000.00, 1000.00};
  std::array departmentTwo{2000.00, 500.00, 500.00};

  std::cout << "department 1:\n";
  for (const double &value : departmentOne) {
    std::cout << value << ' ';
  }
  std::cout << "\n\n";

  std::cout << "department 2:\n";
  for (const double &value : departmentTwo) {
    std::cout << value << ' ';
  }
  std::cout << "\n\n";

  std::array departmentTotal{departmentOne, departmentTwo};

  std::cout << "values of departments:\n";
  for (const auto &department : departmentTotal) {
    for (const double &value : department) {
      std::cout << value << " ";
    }
    std::cout << '\n';
  }
  std::cout << '\n';

  double valueTotal{0};
  for (const auto &department : departmentTotal) {
    for (const double &value : department) {
      valueTotal += value;
    }
  }
  std::cout << "total value:\n" << valueTotal << '\n';
  std::cout << '\n';

  double valueTotalDptm1{0};
  double valueTotalDptm2{0};

  for (const double &value : departmentTotal.at(0)) {
    valueTotalDptm1 += value;
  }
  for (const double &value : departmentTotal.at(1)) {
    valueTotalDptm2 += value;
  }

  std::cout << "total value of department 1:\n" << valueTotalDptm1 << '\n';
  std::cout << "total value of department 2:\n" << valueTotalDptm2 << '\n';

  std::cout << '\n';

  std::array cvm{0.0, 0.0, 0.0};
  for (size_t row{0}; row < departmentTotal.size(); ++row) {
    cvm.at(0) += departmentTotal.at(row).at(0);
    cvm.at(1) += departmentTotal.at(row).at(1);
    cvm.at(2) += departmentTotal.at(row).at(2);
  }

  std::cout << "c\tv\tm\n";
  for (const double &value : cvm) {
    std::cout << value << '\t';
  }
  std::cout << '\n';

  return 0;
}
