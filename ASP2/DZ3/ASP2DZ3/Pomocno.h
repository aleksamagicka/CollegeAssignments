#pragma once
#include <string>
#include <vector>

using namespace std;

static class Pomocno
{
public:
	static vector<string> prvaPermutacija(string rec);
	static vector<string> drugaPermutacija(string rec);
	static vector<string> trecaPermutacija(string rec);

	static vector<char> okolnaSlova(char slovo);
};
