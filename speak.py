from flask import Flask, request, Response
import plivo, plivoxml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Call
engine=create_engine('sqlite:///call.db')
Base.metadata.bind=engine
DBSession=sessionmaker(bind=engine)
session=DBSession()
Yes=1
No=0
app = Flask(__name__)
auth_id = "MANDCZZTUWZDUWNTBHMZ"

@app.route("/forward/", methods=['GET','POST'])
def forward():

    # Generate a Dial XML to forward an incoming call.

    # The phone number of the person calling your Plivo number,
    # we'll use this as the Caller ID when we forward the call.

    from_number = request.args.get('From')
    call_uuid = request.args.get('CallUUID')
    call_status = request.args.get('CallStatus')
    # The number you would like to forward the call to.
    forwarding_number = "919092937238"

    checkcalls=session.query(Call).filter_by(busy=Yes).one()


    #if checkcalls:
     #   pass
    #else:
    print "hello there"
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)