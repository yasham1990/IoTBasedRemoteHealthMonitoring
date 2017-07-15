package org.yasham.rest.heartratelive.database;

import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.Map;

import org.yasham.rest.heartratelive.model.HeartRate;


public class Database {
	
	private static Map<Integer, LinkedHashSet<HeartRate>> heartRates=new HashMap<>();
	
	public static Map<Integer, LinkedHashSet<HeartRate>> getHeartRates(){
		return heartRates;
	}

}
