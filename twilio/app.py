from flask import Flask, request
 
from twilio.rest import Client
 
app = Flask(__name__)
 
# put your own credentials here 
ACCOUNT_SID = 'AC376ba1e447829d9ce2e26c42bb349245' 
AUTH_TOKEN = 'bb67bf84c082628e00e74bf86c780f01' 
 
client = Client(ACCOUNT_SID, AUTH_TOKEN)
 
@app.route('/sms', methods=['POST'])
def send_sms():
    message = client.messages.create(
        to=request.form['To'], 
        from_='+15108638297', 
        body=request.form['Body'],
    )
 
    return message.sid
 
if __name__ == '__main__':
        app.run()
