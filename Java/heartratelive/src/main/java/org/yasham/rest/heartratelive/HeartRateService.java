package org.yasham.rest.heartratelive;

import java.sql.Timestamp;
import java.util.LinkedHashSet;
import java.util.Map;

import javax.ws.rs.core.Response;
import javax.ws.rs.core.Response.Status;

import org.yasham.rest.heartratelive.database.Database;
import org.yasham.rest.heartratelive.model.HeartRate;
import org.yasham.rest.heartratelive.model.StatusMessage;


public class HeartRateService {
	
	private static Map<Integer, LinkedHashSet<HeartRate>> heartRates = Database.getHeartRates();
	
	public Response createHeartRate(HeartRate heartRate) {
		LinkedHashSet<HeartRate> hashSet=heartRates.getOrDefault(heartRate.getUserId(), new LinkedHashSet<HeartRate>());
		heartRate.setTime( Timestamp.valueOf(heartRate.getTimestamp()));
		hashSet.add(heartRate);
		heartRates.put(heartRate.getUserId(), hashSet );
		System.out.println("Created hearrate..........");
		return Response.status(201).entity(heartRate).build();
	}
	
	public Response getHeartRate(int userId) {
		LinkedHashSet<HeartRate> hashSet=heartRates.getOrDefault(userId, new LinkedHashSet<HeartRate>());
		if(hashSet.isEmpty())
		{
			StatusMessage statusMessage = new StatusMessage();
			statusMessage.setStatus(Status.NOT_FOUND.getStatusCode());
			statusMessage.setMessage(String.format("User with ID of %d is not found.", userId));
			return Response.status(404).entity(statusMessage).build();
		}
		HeartRate heartRate=hashSet.iterator().next();
		hashSet.remove(heartRate);
		heartRates.put(userId, hashSet );
		return Response.status(200).entity(heartRate).build();
	}
}
