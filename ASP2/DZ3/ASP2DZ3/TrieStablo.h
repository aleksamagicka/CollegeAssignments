#if !defined(AFX_TRIESTABLO_H__EA14736F_A30C_4DA9_A044_C865B9328099__INCLUDED_)
#define AFX_TRIESTABLO_H__EA14736F_A30C_4DA9_A044_C865B9328099__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#include <stack>

#include "Stablo.h"
#include <vector>

class TrieStablo : public Stablo
{
protected:

	class TrieCvor
	{
		TrieCvor* m_niz_pokazivaca[255];
		TrieCvor* m_roditelj;

		int m_info;
		int m_brojPodstabala;

	public:
		TrieCvor(TrieCvor* roditelj);
		string kljuc;

		TrieCvor(const TrieCvor&)
		{
		}

		TrieCvor& operator=(const TrieCvor&)
		{
		}

		virtual ~TrieCvor();

		TrieCvor* roditelj()
		{
			return m_roditelj;
		}

		TrieCvor* pronadjiPodstablo(char deoKljuca);
		void dodajPodstablo(char deoKljuca, TrieCvor* cvor);
		void ukloniPodstablo(char deoKljuca);

		int brojPodstabala() const { return m_brojPodstabala; }
		int brojPonavljanja() const { return m_info; }

		int dohvatiInfo();
		void postaviInfo(int tekst);

		void poseti(ostream& it, int maxNivo, int nivo);

		string dohvatiKljuc();
		void postaviKljuc(const char* kljuc);

		TrieCvor* jedinoPodstablo();
	};

	TrieCvor* m_koren;

	TrieStablo(const TrieStablo&)
	{
	}

	TrieStablo& operator=(const TrieStablo&)
	{
	}

	TrieCvor* pronadjiCvor(const char* kljuc, stack<TrieCvor*>* stack); // pronalazi cvor koji sadrzi dati kljuc

public:
	TrieStablo();
	virtual ~TrieStablo();

	bool umetni(const char* kljuc) override;
	bool obrisi(const char* kljuc) override;

	void obidji(ostream& it) override;

	int dohvatiInfo(const char* kljuc) override;

	void stampanjePredikcija(vector<pair<int, string>> predikcije);
	void ispisIspravljenih(string kljuc);
	vector<pair<int, string>> nadjiPredikcije(string kljuc);

	void nadjiPredlozene(TrieCvor* cvor, string trenutniPrefiks, vector<TrieCvor*>& spisak);

	vector<pair<int, string>> top3Predikcije(const vector<string>& spisak);
};

#endif // !defined(AFX_TRIESTABLO_H__EA14736F_A30C_4DA9_A044_C865B9328099__INCLUDED_)
