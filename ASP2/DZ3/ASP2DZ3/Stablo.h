#if !defined(AFX_STABLO_H__5F3D5977_5DFA_4D4C_B15E_3DD09CBA589F__INCLUDED_)
#define AFX_STABLO_H__5F3D5977_5DFA_4D4C_B15E_3DD09CBA589F__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#include <IOSTREAM>
using namespace std;

class Stablo
{
protected:

	int m_brCvorova;
	int m_brKljuceva;

	Stablo()
	{
		m_brKljuceva = 0;
		m_brCvorova = 0;
	}


public:

	virtual ~Stablo()
	{
	}

	virtual bool umetni(const char* kljuc) = 0;
	virtual bool obrisi(const char* kljuc) = 0;

	virtual int dohvatiInfo(const char* kljuc) = 0;

	virtual int brojCvorova() { return m_brCvorova; }
	virtual int brojKljuceva() { return m_brKljuceva; }

	virtual void obidji(ostream& it) = 0;

	virtual void ispisiStatistiku(ostream& it)
	{
		it << "Ukupno cvorova: " << brojCvorova() << endl;
		it << "Ukupno kljuceva: " << brojKljuceva() << endl;
	}
};

#endif // !defined(AFX_STABLO_H__5F3D5977_5DFA_4D4C_B15E_3DD09CBA589F__INCLUDED_)
