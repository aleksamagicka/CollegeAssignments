#include "asystem.h"
#include "iostream.h"
#include <stdlib.h>

extern int userMain(int argc, char* argv[]);

int main(int argc, char* argv[]) {
	System::initialize();
	int ret = userMain(argc, argv);
	System::finalize();

	//cout << "stigao ovde..." << endl;
	return ret;
}
