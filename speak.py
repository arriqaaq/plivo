from flask import Flask, request, Response
import plivo, plivoxml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Call
from requests.auth import HTTPBasicAuth
import requests

Yes = 1
No = 0
Done = -1

app = Flask(__name__)
auth_id = "MANDCZZTUWZDUWNTBHMZ"
auth_token = "OTAxYThjNjQzZTZlYWU1ZjkwNjdlNGY1YTEyNjkz"
p = plivo.RestAPI(auth_id, auth_token)
body = "https://s3.amazonaws.com/plivocloud/Trumpet.mp3"
engine=create_engine('sqlite:///call.db')
Base.metadata.bind=engine
DBSession=sessionmaker(bind=engine)
session=DBSession()    
    
@app.route("/forward/", methods=['GET','POST'])
def forward():
    # Generate a Dial XML to forward an incoming call.

    # The phone number of the person calling your Plivo number,
    # we'll use this as the Caller ID when we forward the call.

    from_number = request.args.get('From')
    call_uuid = request.args.get('CallUUID')
    call_status = request.args.get('CallStatus')
    forwarding_number = "919092937238"

    checkcalls=session.query(Call).filter_by(busy=Yes).first()

    if checkcalls:
        newCall=Call(name=call_uuid,status=call_status,busy=No)
        session.add(newCall)
        session.commit()
        response = plivoxml.Response()
        p = response.addPlay(body,loop=True)
        ret_resp = make_response(response.to_xml())
        ret_resp.headers["Content-Type"] = "text/xml"
        print response.to_xml()
        return ret_resp
        
    else:
        print "yayyy"    
        newCall=Call(name=call_uuid,status=call_status,busy=Yes)
        session.add(newCall)
        session.commit()
        params = {
            'callerId': from_number # The phone number to be used as the caller id. It can be set to the from_number or any custom number.
        }
        response = plivoxml.Response()
        d = response.addDial(**params)
        d.addNumber(forwarding_number)
        print response.to_xml()
        return Response(str(response), mimetype='text/xml')

@app.route("/hangup/", methods=['GET','POST'])
def hangup():
    from_number = request.args.get('From')
    call_status = request.args.get('CallStatus')
    print "Hang up status: ",call_status
    call_uuid = request.args.get('CallUUID')
    print "Call UUID is : %s " % (call_uuid)
    editedcall=session.query(Call).filter_by(name=call_uuid).one()
    editedcall.status=call_status
    editedcall.busy=Done
    session.add(editedcall)
    session.commit()
    remcall=session.query(Call).filter_by(busy=No).one()
    url='''https://api.plivo.com/v1/Account/{}/Call/{}/'''.format(auth_id,remcall.call_uuid)
    #tested with requests that user id and password for the api request are the authi id and token
    requests.get(url,auth=HTTPBasicAuth(auth_id, auth_token))
    response = plivoxml.Response()
    print response.to_xml()
    return Response(str(response), mimetype='text/xml')

#Tried this method for transferring call too
#params = {
#        'call_uuid' : 'XXXXXXXXXXXXXXX',
#        'transfer_url': 'http:example.com/transfer_url',
#        }
#response = p.transfer_call(params)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
