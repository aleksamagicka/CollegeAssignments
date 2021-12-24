package com.aleksasavic;

import java.util.ArrayList;

public class RouterInterface
{
	public String Hostname;
	public int ID; // ifIndex
	public String Name; // ifDescr
	public String Type; // ifType
	//public String UpDown; // ifOperStatus
	
	public ArrayList<Integer> InOctets; // ifInOctets
	public ArrayList<Integer> PInOctets;
	public ArrayList<Integer> OutOctets; // ifOutOctets
	public ArrayList<Integer> POutOctets;
	
	public ArrayList<Integer> InUniPkts; // ifInUcastPkts
	public ArrayList<Integer> PInUniPkts;
	public ArrayList<Integer> OutUniPkts; // ifOutUcastPkts
	public ArrayList<Integer> POutUniPkts;
	
	public ArrayList<Integer> InNUniPkts; // ifNUcastPkts
	public ArrayList<Integer> PInNUniPkts;
	public ArrayList<Integer> OutNUniPkts; // ifOutNUcastPkts
	public ArrayList<Integer> POutNUniPkts;
	
	public RouterInterface()
	{
		InOctets = new ArrayList<>();
		PInOctets = new ArrayList<>();
		OutOctets = new ArrayList<>();
		POutOctets = new ArrayList<>();
		InUniPkts = new ArrayList<>();
		PInUniPkts = new ArrayList<>();
		OutUniPkts = new ArrayList<>();
		POutUniPkts = new ArrayList<>();
		InNUniPkts = new ArrayList<>();
		PInNUniPkts = new ArrayList<>();
		OutNUniPkts = new ArrayList<>();
		POutNUniPkts = new ArrayList<>();
	}
	
	void getProtok(ArrayList<Integer> list, ArrayList<Integer> list2)
	{
		if (list.size() < 2)
			list2.add(0);
		
		int prvi = list.get(list.size() - 1);
		int drugi = list.get(list.size() - 2);
		
		list2.add(8*(prvi - drugi)/10);
	}
	
	int l(ArrayList<Integer> list)
	{
		if (list.size() == 0)
			return 0;
		return list.get(list.size() - 1);
	}
	
	public Object[] Row;
	
	public Object[] GetRow()
	{
		return new Object[] {Hostname, ID, Name, Type, l(InOctets), l(PInOctets), l(OutOctets), l(POutOctets),
				l(InUniPkts), l(PInUniPkts), l(OutUniPkts), l(POutUniPkts),
				l(InNUniPkts), l(PInNUniPkts), l(OutNUniPkts), l(POutNUniPkts)};
	}
}

/*
ifIndex - 0
ifDescr - 1
ifType  - 2
ifSpeed - 4
ifInOctets - 9
ifInUcastPkts - 10
ifInNUcastPkts - 11
ifOutOctets - 15
ifOutUcastPkts - 16
ifOutNUcastPkts - 17
*/