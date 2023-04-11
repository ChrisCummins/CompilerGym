#include <iostream>

#include "miniapp/app.pb.h"

int main() {
  MiniApp message;
  message.set_value("Value");

  std::cout << "Hello, " << message.value() << " world!" << std::endl;
}
