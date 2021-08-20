#ifndef _kernel_sem_h_
#define _kernel_sem_h_

#include "aconst.h"
#include "semaphor.h"
#include "pcb.h"
#include "sempthrd.h"

class KernelSem {
public:
	KernelSem(int init, Semaphore *initSemph);
	~KernelSem();

	int wait(Time maxTimeToWait);
	void signal();

	int val() const;

private:
	friend void interrupt timer(...);

	Semaphore *semph;
	int count;

	void releaseBlocked();
	void releaseTimed();

	void timerCleanup();

	List<PCB*> blockedThreads;
	List<SemaphoredThread> timeBlocked;
};

#endif
