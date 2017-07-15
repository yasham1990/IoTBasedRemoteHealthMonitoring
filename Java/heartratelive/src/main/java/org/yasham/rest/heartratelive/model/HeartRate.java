package org.yasham.rest.heartratelive.model;

import java.sql.Timestamp;

public class HeartRate {

	private String heartRate;
	
	private Integer userId;
	
	private Timestamp time;
	
	private String timestamp;
	
	public HeartRate() {
		// TODO Auto-generated constructor stub
	}
	
	public HeartRate(String heartRate, Integer userId, String timestamp) {
		this.heartRate = heartRate;
		this.userId=userId;
		this.timestamp=timestamp;
	}
	
	public Timestamp getTime() {
		return time;
	}

	public void setTime(Timestamp time) {
		this.time = time;
	}

	public String getTimestamp() {
		return timestamp;
	}

	public void setTimestamp(String timestamp) {
		this.timestamp = timestamp;
	}

	public String getHeartRate() {
		return heartRate;
	}

	public Integer getUserId() {
		return userId;
	}

	public void setUserId(Integer userId) {
		this.userId = userId;
	}

	public void setHeartRate(String heartRate) {
		this.heartRate = heartRate;
	}
	
}

