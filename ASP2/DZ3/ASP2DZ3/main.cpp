#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <filesystem>
#include <chrono>

#include "TrieStablo.h"

using namespace std;
namespace fs = std::filesystem;

void napraviPraznoStablo(TrieStablo*& stablo)
{
	stablo = new TrieStablo;
}

void unistavanjeRecnika(TrieStablo*& stablo)
{
	delete stablo;
	stablo = nullptr;
}

bool izmedju(int x, int levo, int desno)
{
	return levo <= x && x <= desno;
}

bool proveriAlfabetski(const string_view& str)
{
	for (char i : str)
	{
		if (!izmedju(i, 97, 122) && !izmedju(i, 65, 90))
			return false;
		
		/*if (i < 0 || i > 255)
			return false;

		if (i == ' ' || i == '.' || i == '@' || i == ':' || i == '(' || i == ')' || i == '!' || i == '#' || i == '$' ||
			i == '&' || i == '%' || i == '"' || i == '\'' || i == '*' || i == '+' || i == '-' || i == '=' || i == '/' ||
			i == ',')
			return false;*/
	}

	return true;
}

void razdeli1(const string_view& str, const string& separator, TrieStablo* stablo)
{
	int pozicijaProslog = 0, trenutnaPozicija;
	do
	{
		trenutnaPozicija = str.find(separator, pozicijaProslog);
		if (trenutnaPozicija == string::npos)
			trenutnaPozicija = str.length();
		string_view token = str.substr(pozicijaProslog, trenutnaPozicija - pozicijaProslog);

		if (!token.empty() && proveriAlfabetski(token))
			stablo->umetni(string(token).c_str());

		pozicijaProslog = trenutnaPozicija + separator.length();
	}
	while (trenutnaPozicija < str.length() && pozicijaProslog < str.length());
}

void ucitajDatoteku(TrieStablo* stablo, const string& imeDatoteke)
{
	ifstream fajl(imeDatoteke);
	string linija;

	int i = 0;

	if (fajl.is_open())
	{
		while (!fajl.eof())
		{
			i++;
			getline(fajl, linija);

			if (i == 3)
			{
				// To je prava linija sa sadrzajem
				razdeli1(string_view(linija), " ", stablo);
			}
		}
		fajl.close();
	}
}

void ucitavanjeDatoteke(TrieStablo* stablo)
{
	cout << "Ime datoteke: ";

	string imeDatoteke;
	cin >> imeDatoteke;

	ucitajDatoteku(stablo, imeDatoteke);
	cout << endl;

	stablo->obidji(cout);
}

void ucitavanjeDatotekaIzFoldera(TrieStablo* stablo)
{
	cout << "Ime foldera: ";
	string imeFoldera;
	cin >> imeFoldera;

	auto pocetak = chrono::high_resolution_clock::now();

	for (const auto& entry : fs::directory_iterator(imeFoldera))
		ucitajDatoteku(stablo, entry.path().string());

	const auto kraj = chrono::high_resolution_clock::now();

	chrono::duration<double> elapsed = kraj - pocetak;

	cout << "Vreme: " << elapsed.count() << endl;
}

void pretragaReci(TrieStablo* stablo)
{
	cout << "Rec za pretragu: ";

	string rec;
	cin >> rec;

	int rezultat = stablo->dohvatiInfo(rec.c_str());
	if (rezultat != -1)
	{
		cout << endl << "Postoji! Prioritet: " << rezultat << endl;
	}
	else
	{
		cout << endl << "Data rec se ne nalazi u recniku!" << endl;
	}
}

void umetanjeReci(TrieStablo* stablo)
{
	cout << "Rec za umetanje: ";

	string rec;
	cin >> rec;

	stablo->umetni(rec.c_str());

	cout << "Novi prioritet: " << stablo->dohvatiInfo(rec.c_str()) << endl;
}

void predvidjanjeReci(TrieStablo* stablo)
{
	cout << "Pocetna rec za predikciju: ";

	string rec;
	cin >> rec;
	cout << endl;

	auto rezultati = stablo->nadjiPredikcije(rec);

	/*for (auto stavka : rezultati)
	{
		cout << stavka.second << " (" << stavka.first << ")" << endl;
	}

	cout << endl;*/
}

void obidjiStablo(TrieStablo* stablo)
{
	//ofstream fajl;
	//fajl.open("izvoz.txt");
	//stablo->obidji(fajl);
	//fajl.close();

	stablo->obidji(cout);
}

int main()
{
	cout << "Aleksa Savic, 595/19, DZ3" << endl;
	cout << "1. Stvaranje praznog recnika" << endl;
	cout << "2. Unistavanje recnika" << endl;
	cout << "3. Ucitavanje datoteke" << endl;
	cout << "4. Ucitavanje svih datoteka iz foldera" << endl;
	cout << "5. Pretrazivanje reci" << endl;
	cout << "6. Umetanje reci" << endl;
	cout << "7. Predvidjanje reci" << endl;
	cout << "8. Obidji stablo" << endl;
	cout << "0. Izlaz" << endl;

	TrieStablo* stablo = nullptr;

	int ulaz = 0;
	bool vrti = true;
	while (vrti)
	{
		cout << "Komanda: ";
		cin >> ulaz;

		switch (ulaz)
		{
		case 0:
			vrti = false;
			break;
		case 1:
			napraviPraznoStablo(stablo);
			break;
		case 2:
			unistavanjeRecnika(stablo);
			break;
		case 3:
			ucitavanjeDatoteke(stablo);
			break;
		case 4:
			ucitavanjeDatotekaIzFoldera(stablo);
			break;
		case 5:
			pretragaReci(stablo);
			break;
		case 6:
			umetanjeReci(stablo);
			break;
		case 7:
			predvidjanjeReci(stablo);
			break;
		case 8:
			obidjiStablo(stablo);
			break;
		default:
			cout << "Nije prepoznata komanda!" << endl;
			break;
		}

		cout << endl;
	}

	return 0;
}
