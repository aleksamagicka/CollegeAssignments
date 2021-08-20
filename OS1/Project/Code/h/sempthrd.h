#include "pcb.h"

// Sluzi za vremenske semafore, cuva blokiran PCB i vreme budjenja u tickovima

class SemaphoredThread {
public:
	SemaphoredThread(PCB *pcb, unsigned long long scheduledWakeupTime);

	// Mora jer se lista buni
	bool operator ==(const SemaphoredThread & st) const { return false; }
private:
	friend class KernelSem;

	PCB *myPCB;
	volatile unsigned long long futureWakeupTime;
};
