package org.yasham.rest.heartratelive.resources;

import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import org.yasham.rest.heartratelive.HeartRateService;
import org.yasham.rest.heartratelive.model.HeartRate;

@Path("/heartrate")
@Consumes(MediaType.APPLICATION_JSON)
@Produces(MediaType.APPLICATION_JSON)
public class HeartRateResource {
	
	HeartRateService heartRateService=new HeartRateService();
	
	@POST
	public Response createOrder(HeartRate heartRate) {
		return heartRateService.createHeartRate(heartRate);
	}
	
	@GET
	public Response getHeartRate(@QueryParam("userId") int userId) {
		return heartRateService.getHeartRate(userId);
	}
	
	@GET
	@Path("/check")
	@Produces(MediaType.TEXT_PLAIN)
	public String getCheckServices() {
		return "Application Works";
	}
	
	public static void main(String[] args) {
		try {
			System.out.println("try");
		} finally {
			System.out.println("finally");
			// TODO: handle finally clause
		}
	}
	

}
