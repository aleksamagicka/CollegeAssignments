#include "idlethrd.h"
#include "asystem.h"
#include "iostream.h"

IdleThread::IdleThread() :
		Thread(512, 1) {
}

void IdleThread::run() {
	while (System::isIdleRunning) {
		/*lock;
		 cout << "idling" << endl;
		 unlock;*/
	}
}
