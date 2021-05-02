import requests
from flask import Flask, request, render_template, jsonify
from flask_mpesa import MpesaAPI
from flask_ngrok import run_with_ngrok

app=Flask(__name__)
# run_with_ngrok(app)

mpesaapi=MpesaAPI(app)

@app.route('/transact/c2b')
def c2b_transact():
    data = {
        "business_shortcode": "174379", #from developers portal
        "passcode": "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919",#from developers portal
        "amount": "1", # choose amount preferrably KSH 1
        "phone_number":"", #phone number to be prompted to pay
        "reference_code": "",#Code to inform the user of services he/she is paying for.
        "callback_url": "[YOUR_URL]", # cllback url should be exposes. for testing putposes you can route on host 0.0.0.0 and set the callback url to be https://youripaddress:yourport/endpoint
        "description": "[Description]" #a description of the transaction its optional
    }
    resp = mpesaapi.MpesaExpress.stk_push(**data)  # ** unpacks the dictionary
    ##use resp to capture the response
    return render_template('home.html')


@app.route('/')
def checkout():
    access_token = "<access token>"
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": "174379",
        "Password": "<base64encoded(174379 + passkey + timestamp )>",
        "Timestamp": "YYYYMMDDHHMMSS",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": "1",
        "PartyA": "<your number>",
        "PartyB": "174379",
        "PhoneNumber": "<your number>",
        "CallBackURL": "<callback_url>",
        "AccountReference": "Test",
        "TransactionDesc": "Test"
    }

    response = requests.post(api_url, json=request, headers=headers)

    print(response.text)
    return response.text


@app.route('/callback',methods=["POST"])
def callback_url():
    #get json data set to this route
    json_data = request.get_json()
    #get result code and probably check for transaction success or failure
    result_code=json_data["Body"]["stkCallback"]["ResultCode"]
    '''message={
        "ResultCode":0,
        "ResultDesc":"success",
        "ThirdPartyTransID":"h234k2h4krhk2"
    }'''

    print(json_data)
    #if result code is 0 you can proceed and save the data else if its any other number you can track the transaction
    return json_data


if __name__ == '__main__':
    app.run('127.0.0.1', port=80, debug=True)
