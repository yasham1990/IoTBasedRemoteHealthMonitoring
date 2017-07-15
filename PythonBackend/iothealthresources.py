import fitbit
from flask import render_template, flash, redirect, session, url_for, request, jsonify, send_from_directory
from random import choice
from flask_oauthlib.client import OAuth
import json
import humanize
import dateutil.parser
from numpy import average
import requests
import logging
from datetime import datetime, timedelta

from flask import Flask, flash
from mysqlconnection import MySQLConnector
from flask_pymongo import PyMongo
import re
from fitbit.api import FitbitOauth2Client,Fitbit
from iHealth import iHealth
import configIhealth as ihealthfg

from requests_oauthlib import OAuth2, OAuth2Session
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
from fitbit.exceptions import (BadResponse, DeleteError, HTTPBadRequest,
                               HTTPUnauthorized, HTTPForbidden,
                               HTTPServerError, HTTPConflict, HTTPNotFound,
                               HTTPTooManyRequests)
from fitbit.utils import curry


client_id = ihealthfg.CLIENT_ID
client_secret = ihealthfg.CLIENT_SECRET
callback = ihealthfg.CALLBACK_URI
api = iHealth(client_id, client_secret, callback)


app = Flask(__name__)
mysql = MySQLConnector(app, 'cmpe280')
app.secret_key = "TheSecretLifeOfTheKeys"
logger = logging.getLogger('mylogger')

app.config['MONGO_URI'] = 'mongodb://34.223.225.244:27017/ihealth'
mongo = PyMongo(app)

app.config['MONGO2_URI'] = 'mongodb://34.223.225.244:27017/fitbit'
mongo2 = PyMongo(app,config_prefix='MONGO2')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#Minimum 8 characters at least 1 Uppercase Alphabet, 1 Lowercase Alphabet and 1 Number:
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]+$')

heartdata=[]
notificationUpdate={}
notificationUpdate['recommedation']=''
notificationUpdate['calorieExceeds']=''
notificationUpdate['calorieAvailable']=''


try:
    from urllib.parse import urlencode
except ImportError:
    # Python 2.x
    from urllib import urlencode

import helper

CONVERSION = {
    "en_US": "Pounds"
}


@app.route('/getrecommendation')
def getRecommendation():
    try:
	data=[["N/A","Server not Found"]]
        url = 'http://34.223.225.244:5000/recommend'
        params = dict(calorie=session['availableCalorie'])
	if int(session['availableCalorie']) >= 0:
		resp = requests.get(url=url, params=params)
		if resp.status_code == 404:
		    data = {"0","Server not Found"}
		else:
		    data = json.loads(resp.text)
	else:
		data = [["0","Calorie Goal For the Day Exceeded."]]
    except Exception as error : 
	logging.exception("message")
    return render_template('recommendation.html', data=data)

@app.route('/')
def getDashboardData():
    try:
        if not session.get('fitbit_keys', False):
            return redirect(url_for('start'))
        userprofile_id = session['user_profile']['user']['encodedId']
        stepsData = getDataForActivities(userprofile_id, 'steps', period='1d', return_as='raw')[0]['value']
	weights = fit.get_bodyweight(user_id=userprofile_id, period='1m')['weight']
	weight_last = weights[-1]['weight']
	if weight_last is not None:
		session['weight']=weight_last
        caloriesData = getDataForActivities(userprofile_id, 'calories', period='1d', return_as='raw')[0]['value']

        heartRate =65
        weights = getDataForActivities(userprofile_id, 'weight', period='1w', return_as='raw')
        weight0 = weights[0]['value']
        weightn = weights[-1]['value']
        diff = (float(weight0) - float(weightn))
        bodyMassIndex=int(session['bmi'])
        helper.getEstimationForCalorie(caloriesData)
        if diff > 0:
            diff = "+" + str(diff)
        else:
            diff = str(diff)
        sleep = getDataForActivities(userprofile_id, 'timeInBed', period='1d', return_as='raw')[0]['value']
        chartdata = getDataForActivities(userprofile_id, 'steps', period='1w', return_as='raw')
        weight_unit = CONVERSION[session['user_profile']['user']['weightUnit']]

        itemsCur = mongo.db.ihealthbps
        bpreadings = itemsCur.find({}).sort([("measurement_time", -1)]).limit(1)
        output = []
        lp=""
        hp=""
        caloriesConsumed=session['caloriesConsumed']
        caloriesEstimated=session['availableCalorie']
        for bp in bpreadings:
            lp=str(bp['LP'])
            hp=str(bp['HP'])
            mesurementTime=str(bp['measurement_time'])

        return render_template('home.html', Bmi = bodyMassIndex, caloriesConsumed=caloriesConsumed, caloriesEstimated=caloriesEstimated, heartRate=heartRate,steps=stepsData, calories=caloriesData, weight=diff, sleep=sleep, chartdata=chartdata,weights=weights, weight_unit=weight_unit,cqm=cqmDataCheck(),lp=lp,hp=hp,mesurementTime=mesurementTime)
    except Exception as error : 
	logging.exception("message")

@app.route('/profileDetails')
def profileDetails():
    if not session.get('fitbit_keys', False):
        return redirect(url_for('start'))
    return render_template('profileDetails.html')


@app.route('/profileDetailsUpdate', methods=["POST"])
def profileDataUpdate():
    try:
	session['weight'] = request.form['curweight']
	session['goal'] = request.form['goalweight']
	heightBmi=float(session['height'])*float(session['height'])
	session['bmi']=int((float(session['weight'])*703)/heightBmi)
	query = "Update UserProfile set Weight= :weight, goal=:goal,bmi=:bmi WHERE UserId = :userId"
	data = {
	"weight" : session['weight'],
	"goal" : session['goal'],
	"bmi" : session['bmi'],
	"userId" : session['user_Id']
	}
	mysql.query_db(query, data)
	userprofile_id = session['user_profile']['user']['encodedId']
	caloriesBurned = getDataForActivities(userprofile_id, 'calories', period='1d', return_as='raw')[0]['value']
	helper.getEstimationForCalorie(caloriesBurned)
	print("Updated Successfully")
    except Exception as error : 
	logging.exception("message")
    return redirect(url_for('dashboard'))


@app.route('/calories')
def getCaloriesData():
    try:
	if not session.get('fitbit_keys', False):
		return redirect(url_for('start'))
	monthlyCalorieData = fit.time_series('activities/calories', base_date='today',period='1m')['activities-calories']
    except Exception as error : 
	logging.exception("message")
    return render_template('calories.html', monthlyCalorieData=monthlyCalorieData)


@app.route('/users/new', methods=["POST"])
def create():
    try:
	result = []
	session['email'] = request.form['email']
	session['password'] = request.form['password']
	session['name'] = request.form['name']
    	session['type'] = request.form['type']
	if len(result) == 0:
		password = session['password']
		query = "INSERT INTO users ( Name, EmailId, Password, Type) VALUES (:name,:email,:password,:type)"
		data = {
		    "email" : session['email'],
		    "password" : session['password'],
		    "name" : session['name'],
            "type" : session['type']
		}
		mysql.query_db(query, data)
		query1 = "SELECT userId FROM users WHERE EmailId = :email"
		data = { "email" : session['email']}
		session['user_Id'] = mysql.query_db(query1,data)[0]['userId']
		return redirect(url_for('registration1'))
	else: 
		for message in result:
		    flash(message,'error')
    except Exception as error : 
	logging.exception("message")
    return redirect(url_for('registration'))


@app.route('/users/profile', methods=["POST"])
def userProfile():
    try:
	session['height'] = request.form['height']
	session['heightinch'] = request.form['heightinch']
	session['gender'] = request.form['gender']
	session['weight'] = request.form['weight']
	session['goal'] = request.form['goal']
	session['age'] = request.form['age']
	heightBmi=((float(request.form['height'])*12)+float(request.form['heightinch']))*((float(request.form['height'])*12)+float(request.form['heightinch']))
	print("heightBmi..... ")
	print(heightBmi)
	session['bmi']=int((float(request.form['weight'])*703)/heightBmi)
	print(session['bmi'])
	query = "INSERT INTO UserProfile ( Weight, Height, Goal, Gender, BMI, Age, UserId) VALUES (:weight, :height,:goal,:gender,:bmi,:age,:userId)"
	data = {
	"weight" : session['weight'],
	"height" : str(int(session['height'])*12+int(session['heightinch'])),
	"goal" : session['goal'],
	"gender" : session['gender'],
	"bmi" : session['bmi'],
	"age" : session['age'],
	"userId" : session['user_Id']
	}
	mysql.query_db(query, data)
	session.pop('height')
	session.pop('heightinch')
	session.pop('goal')
	session.pop('age')
	session.pop('bmi')
	flash("Registered Successfully",'success')
    except Exception as error : 
	    logging.exception("message")
    return redirect(url_for('signin'))
    

@app.route('/users/login', methods=["POST"])
def newlogin():
    try:
    	error = None
	email = request.form['email']
	password = request.form['password']
    	type = request.form['type']
	query = "SELECT * FROM users WHERE EmailId = :email and Type=:type LIMIT 1"
	data = { "email": email,
    "type" : type
    }
	user = mysql.query_db(query,data)
	if user:
		if user[0]['Password']== password :
		    print "LOGIN SUCCESSFUL"
        	    session['email']=email
                    session['type']=type
                    session['user_Id']=user[0]['UserId']
		    error = "LOGIN SUCCESSFUL"
		    return redirect(url_for('customurl1'))
		else:
		    print "Invalid Credentials."
		    error = "Invalid Credentials."
    		    return redirect(url_for('signin',error=error))
	else:
		print "LOGIN UNSUCCESSFUL"
		error = "Invalid Credentials."
		flash("Invalid Credentials.",'error')
    		return redirect(url_for('signin',error=error))
    except Exception as error : 
	logging.exception("message")

@app.route('/users/checkmobilelogin', methods=['POST'])
def checkmobilelogin():
    print("here=========================")
    try:
    	error = None
	email = request.form['email']
	password = request.form['password']
    	#type = request.form['type']
	query = "SELECT * FROM users WHERE EmailId = :email and Type='Patient' LIMIT 1"
	data = { "email": email}
	user = mysql.query_db(query,data)
        output = []
	if user:
		if user[0]['Password']== password :
            		output.append({'UserId':user[0]['UserId']})
            		return jsonify(output)
		else:
            		output.append({'UserId':''})
            		return jsonify(output)
	else:
		output.append({'UserId':''})
        return jsonify(output)
    except Exception as error : 
	logging.exception("message")


@app.route('/food')
def foodEntry():
    return render_template('food_entry.html')

@app.route('/signin')
def signin():
    error=''
    if 'error' in request.args:
        error = request.args.get('error')
    return render_template('login.html',error=error)

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/registration1')
def registration1():
    return render_template('registration1.html')

@app.route('/heartrate')
def heartRate():
    try:
    	print(heartdata)
    except Exception as error :
	logging.exception("message")
        print("...............here................................")
    	return render_template('heartrate.html', heartdata=heartdata)
    return render_template('heartrate.html', heartdata=heartdata)


@app.route('/heartrateDetail')
def heartrateDetail():
    return render_template('heartrateDetail.html')

@app.route('/dashboard')
def dashboard():
    session['functionName']='OnDashboard'
    return redirect(url_for('getDashboardData'))


@app.route('/logout')
def logout():
    try:
    	session.clear()
    except Exception as error :
	logging.exception("message")
    return redirect(url_for('signin'))

@app.route('/addEmergencyContacts', methods=["POST"])
def addEmergencyContacts():
    emergencyCont=""
    try:
        #userId=20
        query = "Insert into EmergencyContacts (UserId,Name,Relation, Phone, Email,Address, Phone2) values (:userId, :Name, :Relation,:Phone, :Email,:Address,:Phone2)"
        data = {
            "userId":session['user_Id'],
            "Name" : request.form["Name"],
            "Relation" : request.form["Relation"],
            "Phone" : request.form["Phone"],
            "Email" : request.form["Email"],
            "Address" : request.form["Address"],
            "Phone2" : request.form["Phone2"]
        }
        mysql.query_db(query, data)

    except Exception as error :
	    logging.exception("message")
    return redirect(url_for('emergencycontacts'))

@app.route('/addEmergencyContactsView')
def addEmergencyContactsView():
    return render_template('emergencycontactsadd.html')

@app.route('/emergencyContacts')
def emergencycontacts():
    emergencyCont=""
    try:
        print("emergency is...")
        #userId=20
        query = "SELECT id,UserId,Name,Relation, Phone, Email,Address, Phone2 FROM EmergencyContacts WHERE UserId = :userId"
        data1 = { "userId" : session['user_Id']}
        emergencyCont = mysql.query_db(query,data1)
	
    except Exception as error :
	    logging.exception("message")
    return render_template('emergency.html', data=emergencyCont)

@app.route('/deleteEmergencyContacts')
def deleteEmergencycontacts():
    emergencyCont=""
    try:
        #userId=20
        query = "delete from EmergencyContacts where UserID=:userId and id=:Id"
        data = { 
            "userId":session['user_Id'],
            "Id" : request.args.get("id")
        }
        mysql.query_db(query, data)


    except Exception as error :
	    logging.exception("message")
    return redirect(url_for('emergencycontacts'))

@app.route('/addAllergyView')
def addAllergyView():
    return render_template('allergyadd.html')

@app.route('/addMedicalHistoryView')
def addMedicalHistoryView():
    return render_template('medicalhistoryadd.html')

@app.route('/addVaccinationView')
def addVaccinationView():
    return render_template('vaccinationadd.html')

@app.route('/addMedicalHistory', methods=["POST"])
def addMedicalHistory():
    emergencyCont=""
    try:
        #userId=20
        query = "INSERT INTO MedicalHistoryRecord (UserId,doc_visit_date,doc_name,primary_doc,mode_of_visit,body_weight,blood_presure_systolic,blood_presure_diastolic,temperature,prescribed_medicaltest_drugs,comments_from_doc) VALUES (:userId,:doc_visit_date,:doc_name,:primary_doc,:mode_of_visit,:body_weight,:blood_presure_systolic,:blood_presure_diastolic,:temperature,:prescribed_medicaltest_drugs,:comments_from_doc )"
        data = {
            "userId":session['user_Id'],
            "doc_visit_date" : request.form["doc_visit_date"],
            "doc_name" : request.form["doc_name"],
            "primary_doc" : request.form["primary_doc"],
            "mode_of_visit" : request.form["mode_of_visit"],
            "body_weight" : request.form["body_weight"],
            "blood_presure_systolic" : request.form["blood_presure_systolic"],
            "blood_presure_diastolic" : request.form["blood_presure_diastolic"],
            "temperature" : request.form["temperature"],
            "prescribed_medicaltest_drugs" : request.form["prescribed_medicaltest_drugs"],
            "comments_from_doc" : request.form["comments_from_doc"]
        }
        mysql.query_db(query, data)
    except Exception as error :
	    logging.exception("message")
    return redirect(url_for('medicalHistory'))

@app.route('/addAllergy', methods=["POST"])
def addAllergy():
    emergencyCont=""
    try:
        #userId=20
        query = "Insert into Allergy (UserId,allergy_date,allergy_name,reaction,severity) values (:userId,:allergy_date, :allergy_name, :reaction,:severity)"
        data = {
            "userId":session['user_Id'],
            "allergy_date" : request.form["allergy_date"],
            "allergy_name" : request.form["allergy_name"],
            "reaction" : request.form["reaction"],
            "severity" : request.form["severity"]
        }
        mysql.query_db(query, data)
    except Exception as error :
	    logging.exception("message")
    return redirect(url_for('medicalHistory'))

@app.route('/addVaccination', methods=["POST"])
def addVaccination():
    emergencyCont=""
    try:
        #userId=20
        query = "Insert into VaccinationImmunization (UserId,VaccinationImmunization_date,VaccinationImmunization_name,VaccinationImmunization_type,VaccinationImmunization_dose_qantity) values (:userId,:VaccinationImmunization_date, :VaccinationImmunization_name, :VaccinationImmunization_type,:VaccinationImmunization_dose_qantity)"
        data = {
            "userId":session['user_Id'],
            "VaccinationImmunization_date" : request.form["VaccinationImmunization_date"],
            "VaccinationImmunization_name" : request.form["VaccinationImmunization_name"],
            "VaccinationImmunization_type" : request.form["VaccinationImmunization_type"],
            "VaccinationImmunization_dose_qantity" : request.form["VaccinationImmunization_dose_qantity"]
        }
        mysql.query_db(query, data)
    except Exception as error :
	    logging.exception("message")
    return redirect(url_for('medicalHistory'))

@app.route('/medicalHistory')
def medicalHistory():
    emergencyCont=""
    try:
        print("history is...")
        #userId=20
        query = "SELECT id,UserId,doc_visit_date,doc_name,primary_doc,mode_of_visit,body_weight,blood_presure_systolic,blood_presure_diastolic,temperature,prescribed_medicaltest_drugs,comments_from_doc FROM MedicalHistoryRecord WHERE UserId = :userId"
        data1 = { "userId" : session['user_Id']}
        medicalHistory = mysql.query_db(query,data1)

        query = "SELECT id,UserId,VaccinationImmunization_date,VaccinationImmunization_name,VaccinationImmunization_type,VaccinationImmunization_dose_qantity FROM VaccinationImmunization WHERE UserId = :userId"
        data1 = { "userId" : session['user_Id']}
        vaccination = mysql.query_db(query,data1)

        query = "SELECT id,UserId,allergy_date,allergy_name,reaction,severity FROM Allergy WHERE UserId = :userId"
        data1 = { "userId" : session['user_Id']}
        allergy = mysql.query_db(query,data1)
	
    except Exception as error :
	    logging.exception("message")
    return render_template('medicalhistory.html', allergy=allergy, medicalHistory=medicalHistory,vaccination=vaccination)

@app.route('/deleteAllergy')
def deleteAllergy():
    emergencyCont=""
    try:
        #userId=20
        query = "delete from Allergy where UserID=:userId and id=:Id"
        data = { 
            "userId":session['user_Id'],
            "Id" : request.args.get("id")
        }
        mysql.query_db(query, data)

    except Exception as error :
	    logging.exception("message")
    return redirect(url_for('medicalHistory'))

@app.route('/deleteMedicalHistory')
def deleteMedicalHistory():
    emergencyCont=""
    try:
        #userId=20
        query = "delete from MedicalHistoryRecord where UserID=:userId and id=:Id"
        data = { 
            "userId":session['user_Id'],
            "Id" : request.args.get("id")
        }
        mysql.query_db(query, data)

    except Exception as error :
	    logging.exception("message")
    return redirect(url_for('medicalHistory'))

@app.route('/deleteVaccination')
def deleteVaccination():
    emergencyCont=""
    try:
        #userId=20
        query = "delete from VaccinationImmunization where UserID=:userId and id=:Id"
        data = { 
            "userId":session['user_Id'],
            "Id" : request.args.get("id")
        }
        mysql.query_db(query, data)

    except Exception as error :
	    logging.exception("message")
    return redirect(url_for('medicalHistory'))

@app.route('/customurl')
def customurl():
    if 'code' in request.args:
        code = request.args.get('code')
    return render_template('customurl.html')

@app.route('/customurl1')
def customurl1():
    try:
        print("user profile is....................")
        print(session['user_Id'])
        if session['type']=='Doctor':
            query = "SELECT users.UserId,Name,EmailId,(Select clientId from DeviceCredentials where redirectUri!=:redirectUri) as clientId,(Select secretKey from DeviceCredentials where redirectUri!=:redirectUri) as secretKey,(Select redirectUri from DeviceCredentials where redirectUri!=:redirectUri) as redirectUri FROM users  where users.UserId!=:userId and users.Type!=:type";
            data1 = { "type" : 'Doctor',"redirectUri":'http://54.69.139.242:3000/customurl',"userId" : session['user_Id']}
            userProfile = mysql.query_db(query,data1)
        else:
            query = "SELECT users.UserId,Name,EmailId,(Select clientId from DeviceCredentials where redirectUri!=:redirectUri) as clientId,(Select secretKey from DeviceCredentials where redirectUri!=:redirectUri) as secretKey,(Select redirectUri from DeviceCredentials where redirectUri!=:redirectUri) as redirectUri FROM users where users.UserId=:userId";
            data1 = { "redirectUri":'http://54.69.139.242:3000/customurl',"userId" : session['user_Id']}
            userProfile = mysql.query_db(query,data1)
	
    except Exception as error :
	    logging.exception("message")
    return render_template('customurl.html', userProfile=userProfile)

@app.route('/updateCredentials', methods=['POST'])
def updateCredentials():
    try:
        obj=request.get_json(force=True)
        query = "SELECT Name,EmailId,Type FROM users where UserId=:userId";
        data = { "userId" : obj['userId']}
        user = mysql.query_db(query,data)
        if user:
            session['email'] =  user[0]['EmailId']
            session['user_Id'] = obj['userId'];
            session['typeUser'] = user[0]['Type'];
            session['name']= user[0]['Name']
            return json.dumps({'status':'NOT OK'});
	return json.dumps({'status':'OK'});
    except Exception as error :
	    logging.exception("message")
    return render_template('customurl.html', userProfile=userProfile)

# Filters
# ----------------------------

@app.template_filter()
def natural_time(datetime):
    """Filter used to convert Fitbit API's iso formatted text into
    an easy to read humanized format"""
    a = humanize.naturaltime(dateutil.parser.parse(datetime))
    return a



@app.template_filter()
def natural_number(number):
    """ Filter used to present integers cleanly """
    a = humanize.intcomma(number)
    return a

@app.route('/authorize')
def checkCredentials():
    r = api.checkCredentials()
    return redirect(r.url)

@app.route('/bloodpressure', methods=['GET'])
def get_bp():
    try:
        itemsCur = mongo.db.ihealthbps
        bpreadings = itemsCur.find({}).sort([("measurement_time", -1)]).limit(1)
        output = []
        for bp in bpreadings:
            output.append({'LP':bp['LP'],'HP':bp['HP']})
    except Exception as error : 
	logging.exception("message")
    return jsonify({'result' : output})

@app.route('/ihealth_auth_callback/')
def ihealth_auth_callback():
    try:
        output = []
        itemsCur = mongo.db.ihealthbps
        bpreadings = itemsCur.find({}).sort([("measurement_time", -1)]).limit(1)
                
        dateStart=None
        for bp in bpreadings:
            dateStart = str(bp['MDate'])
        r = api.ihealth_auth_callback()
        if dateStart is not None:
            result = api.getBp(dateStart)
        else:
            result = api.getBp('')
        d = json.loads(result)
       
        print d
	for doc in d["BPDataList"]:
            if str(doc['MDate'])!=dateStart:
                print("here.........................................")
                doc['userId'] = session['user_Id']
            print("here.........................................")
            itemsCur.insert(doc)
    except Exception as error : 
	    logging.exception("message")
    return redirect(url_for('getDashboardData'))

@app.route('/cqmDataCheck', methods=['GET'])
def cqmDataCheck():
    try:
        h='Essential Hypertension'
        e='Encounter'
        o='Office Visit'
        o1='Face-to-Face Interaction'
        o2='Preventive Care Services - Established Office Visit 18 and Up'
        o2='Preventive Care Services-Initial Office Visit, 18 and Up'
        o3='Home Healthcare Services'
        o4='Annual Wellness Visit'

        p='Pregnancy'
        p1='End Stage Renal Disease'
        p2='Chronic Kidney Disease, Stage 5'
       
        query = "select * from users,CqmOccurence,MeasurementPeriod,UserProfile,CqmEvents where users.UserId=CqmEvents.UserId and users.UserId=CqmOccurence.UserId and users.UserId=UserProfile.UserId and users.UserId=:userId and AGE>18 and AGE<85 and (CqmOccurence.Type=:h and (DATE_ADD(MeasurementPeriod.StartDate, INTERVAL 6 MONTH)<CqmOccurence.EndDate OR (CqmOccurence.EndDate>MeasurementPeriod.StartDate AND MeasurementPeriod.StartDate>=CqmOccurence.StartDate))) AND CqmEvents.Type=:e AND CqmEvents.Name in (:o,:o1,:o2,:o3,:o4) AND CqmEvents.EndDate>MeasurementPeriod.StartDate AND CqmOccurence.Type not in (:p,:p1,:p2)"
        data = { "userId": session['user_Id'],
        "h":h,
        "e":e,
        "o":o,
        "o1":o1,
        "o2":o2,
        "o3":o3,
        "o4":o4,
        "p":p,
        "p1":p1,
        "p2":p2 }
        user = mysql.query_db(query,data)
        if user:
            print "--------------------------------"
            itemsCur = mongo.db.ihealthbps
            bpreadings = itemsCur.find({"userId":session['user_Id']}).sort([("measurement_time", -1)]).limit(1)
            output = []
            for bp in bpreadings:
                if int(bp['LP'])<110 and int(bp['HP'])<150:
                    query1="select * from users,CqmEvents where  users.UserId=CqmEvents.UserId AND users.UserId=:userId  AND CqmEvents.Type in (:e) AND CqmEvents.Name in (:o,:o1,:o2,:o3,:o4)"
                    data1 = { "userId": session['user_Id'],
                    "e":e,
                    "o":o,
                    "o1":o1,
                    "o2":o2,
                    "o3":o3,
                    "o4":o4,}
                    cqmImprovement = mysql.query_db(query1,data1)
                    if cqmImprovement:
                        return "Health Improved"
                    else:
                        return "Health Not Improved"
            
    except Exception as error : 
	    logging.exception("message")
    return "Patient Not Considered For CQM Check"

@app.route('/steps')
def steps():
    try:
        if not session.get('fitbit_keys', False):
            return redirect(url_for('start'))
        userprofile_id = session['user_profile']['user']['encodedId']
        asteps = getDataForActivities(userprofile_id, 'steps', period='max', return_as="raw")
        year_steps = getDataForActivities(userprofile_id, 'steps', period='1y', return_as="raw")
        msteps = getDataForActivities(userprofile_id, 'steps', period='1m', return_as="raw")
        wsteps = getDataForActivities(userprofile_id, 'steps', period='1w', return_as="raw")
        dsteps = getDataForActivities(userprofile_id, 'steps', period='1d', return_as="raw")
        dataStatsbar = helper.getStatsBar(asteps,msteps,dsteps)
        boxplot_data = helper.cycleMonth(helper.dataClean(asteps))
        chartsData=helper.getChartsData(asteps,year_steps,msteps,wsteps,boxplot_data)
    except Exception as error : 
	logging.exception("message")
    return render_template('statpage.html', title="Steps", statsbar=dataStatsbar, charts=chartsData, all_steps=asteps, year_steps=year_steps, month_steps=msteps, week_steps=wsteps, day_steps=dsteps, boxplot_data=boxplot_data)

@app.route('/fooditems', methods=['GET'])
def get_items():
    try:
        print("here......................")
        keyword="^"+request.args.get('keyword')+".*"
        itemsCur = mongo2.db.food_data
        abc = itemsCur.find({"name":{"$regex":keyword, "$options" : "-i" }},{"name":1,"_id":0}).limit(10)
        output = []
        for doc in abc:
            output.append({'name':doc['name']})
    except Exception as error : 
	logging.exception("message")
    return jsonify({'result' : output})

@app.route('/fooditemsadd', methods=["POST"])
def fooditemsadd():
    try:
        fooditemname = request.form['fooditemname']
        foodquantity = request.form['qauntity']
    	fooddata = mongo2.db.food_data
        docResult = fooddata.find({"name":fooditemname},{"_id":0,"__v":0});
        for doc in docResult:
            calEstimate = int(doc['calories'])
        session['calorieEst'] = int((float(foodquantity)*calEstimate)/100)
        query = "INSERT INTO FoodEntry ( Item, Quantity, TimeStamp, UserId, calorieEst) VALUES (:foodname, :foodquantity, CURDATE(),:userId, :calorieEst)"
        data = {
            "foodname" : fooditemname,
            "foodquantity" : foodquantity,
            "userId" : session['user_Id'],
            "calorieEst" : session['calorieEst']
        }
        mysql.query_db(query, data)
	userprofile_id = session['user_profile']['user']['encodedId']
	caloriesBurned = getDataForActivities(userprofile_id, 'calories', period='1d', return_as='raw')[0]['value']
	helper.getEstimationForCalorie(caloriesBurned)
	session['functionName']='FoodEntry'
    except Exception as error : 
	logging.exception("message")
    return redirect(url_for('dashboard'))

@app.route('/login')
def login():
    try:
	if 'email' in session:
        	email=session['email']
		print("email is...")
		print(email)
	else:
		email = 'yasham@gmail.com'
        	session['email'] = email
        if 'access-token' in request.args:
            access_token = request.args.get('access-token')
        if 'refresh-token' in request.args:
            refresh_token = request.args.get('refresh-token')
        if 'userId' in request.args:
            user_key = request.args.get('userId')
        if 'secretKey' in request.args:
            user_secret = request.args.get('secretKey')
        global fit
        fit=Fitbit(user_key,user_secret,access_token=access_token, refresh_token=refresh_token)
        session['fitbit_keys'] = (email, user_key, user_secret)
        query = "SELECT userId,Type FROM users WHERE EmailId = :email"
        data = { "email" : email}
        userId = mysql.query_db(query,data)[0]['userId']

        session['user_Id'] = userId;
        session['typeUser'] = mysql.query_db(query,data)[0]['Type'];
        query1 = "SELECT Weight, Gender, Height, Goal, BMI, Age FROM UserProfile WHERE UserId = :userId"
        data1 = { "userId" : userId}
        userProf = mysql.query_db(query1,data1)[0]
	if userProf is not None:
		session['weight'] = userProf['Weight']
		session['height'] = userProf['Height']
		session['gender'] =userProf['Gender']
		session['goal'] = userProf['Goal']
		session['bmi'] = userProf['BMI']
		session['age'] = userProf['Age']
	else:
        	print("userId is...")
        session['user_profile'] = fit.user_profile_get()
	session['functionName']='OnLogin'
    except Exception as error :
	logging.exception("message")
    return redirect(url_for('getDashboardData'))

def getDataForActivities(user_id, resource, period='1w', return_as='json'):
    """ Function to pull data from Fitbit API and return as json or raw specific to activities """
    global dash_resource
    app.logger.info('resource, %s, %s, %s, %s, %s' %
                    (user_id, resource, period, return_as, request.remote_addr))

    ''' Use  API to return resource data '''

    slash_resource = 'activities/' + resource

    colors = (
        'yellow',
        'green',
        'red',
        'blue',
        'mediumGray',
        'aqua',
        'orange',
        'lightGray')

    datasequence_color = choice(colors)

    if period in ('1d', '1w', '1m'):
        graph_type = 'bar'
    else:
        graph_type = 'line'

    # Activity Data
    if resource in ('distance',
                    'steps',
                    'heart',
                    'floors',
                    'calories',
                    'elevation',
                    'minutesSedentary',
                    'minutesLightlyActive',
                    'minutesFairlyActive',
                    'minutesVeryActive',
                    'activeScore',
                    'activityCalories'):
        slash_resource = 'activities/' + resource
        dash_resource = 'activities-' + resource

    # Sleep Data
    if resource in ('startTime',
                    'startTime',
                    'timeInBed',
                    'minutesAsleep',
                    'awakeningsCount',
                    'minutesAwake',
                    'minutesToFallAsleep',
                    'minutesAfterWakeup',
                    'efficiency'):
        slash_resource = 'sleep/' + resource
        dash_resource = 'sleep-' + resource

    if resource in ('weight',
                    'bmi',
                    'fat'):
        slash_resource = 'body/' + resource
        dash_resource = 'body-' + resource

    the_data = fit.time_series(
        slash_resource, base_date='today', period=period)[dash_resource]

    if return_as == 'raw':
        return the_data
    if return_as == 'json':
        return jsonify(helper.output_json(the_data, resource, datasequence_color, graph_type))

@app.route('/weight')
def weight():
    try:
	if not session.get('fitbit_keys', False):
		return redirect(url_for('start'))
	userprofile_id = session['user_profile']['user']['encodedId']
	unit_of_weight = CONVERSION[session['user_profile']['user']['weightUnit']]
	dataOfWeight = fit.get_bodyweight(user_id=userprofile_id, period='1m')['weight']
	weightOfAll = getDataForActivities(userprofile_id, 'weight', period='max', return_as='raw')
	yw = getDataForActivities(userprofile_id, 'weight', period='1y', return_as='raw')
	mw = getDataForActivities(userprofile_id, 'weight', period='1m', return_as='raw')
	ww = getDataForActivities(userprofile_id, 'weight', period='1w', return_as='raw')
	chartdata = helper.cycleDay(dataOfWeight, 'weight')
	plotOf_Box = helper.cycleMonth(weightOfAll)
	cycleOfYear = helper.cycleYear(weightOfAll)
	periods = helper.periodsIntervals(weightOfAll, yw, mw, ww)
	wm = max([d.get('value') for d in weightOfAll])
	wmin = min([d.get('value') for d in weightOfAll])
	wl = dataOfWeight[-1]['weight']
	mm = max([d.get('value') for d in mw])
	barOfStats=helper.getWeightStatsBar(wm,wmin,mm,wl)
    	dataForcharts=helper.getWeightCharts()
    except Exception as error : 
	logging.exception("message")
    return render_template('weight.html', weights=dataOfWeight, weight_unit=unit_of_weight, chartdata=chartdata,
                           all_weight=weightOfAll, boxplot=plotOf_Box, yearcycle=cycleOfYear, periods=periods,
                           statsbar=barOfStats, charts=dataForcharts)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 404


@app.route('/getUserProfileMobile', methods=['Get'])
def getUserProfileMobile():
    try:
        userId=request.args.get('userId')
	output=[]
	query = "SELECT Name,EmailId,Weight, Gender, Height, Goal, BMI, Age FROM UserProfile,users WHERE UserProfile.UserId=users.UserId and users.UserId = :userId"
        data = { "userId" : userId}
        userProf = mysql.query_db(query,data)[0]
	if userProf is not None:
        	output.append({'UserId':userId,'EmailId':userProf['EmailId'],'Name':userProf['Name'],'Height':userProf['Height'],'Weight':userProf['Weight'],'Gender':userProf['Gender'],'Goal':userProf['Goal'],'BMI':userProf['BMI'],'Age':userProf['Age']})
            	return jsonify(output)
	else:
	    output.append({'UserId':''})
            return jsonify(output)
    except Exception as error : 
	logging.exception("message")

@app.route('/emergencyContactsMobile', methods=['Get'])
def emergencyContactsMobile():
    output=[]
    try:
        userId=request.args.get('userId')
        print("emergency is...")
        query = "SELECT id,UserId,Name,Relation, Phone, Email,Address, Phone2 FROM EmergencyContacts WHERE UserId = :userId"
        data1 = { "userId" : userId}
        emergencyCont = mysql.query_db(query,data1)[0]
	
    	if emergencyCont is not None:
        	output.append({'UserId':userId,'Email':emergencyCont['Email'],'Name':emergencyCont['Name'],'Address':emergencyCont['Address'],'Relation':emergencyCont['Relation'],'Phone':emergencyCont['Phone'],'Phone2':emergencyCont['Phone2']})
            	return jsonify(output)
	else:
	    output.append({'UserId':''})
            return jsonify(output)
    except Exception as error : 
	logging.exception("message")
