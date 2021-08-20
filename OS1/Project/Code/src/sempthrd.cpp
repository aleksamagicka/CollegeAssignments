#include "sempthrd.h"

SemaphoredThread::SemaphoredThread(PCB *pcb,
		unsigned long long scheduledWakeupTime) :
		myPCB(pcb), futureWakeupTime(scheduledWakeupTime) {
}
