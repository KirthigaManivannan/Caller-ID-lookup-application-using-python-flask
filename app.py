from flask import Flask, render_template, request
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

app = Flask(__name__)


TWILIO_ACCOUNT_SID = #replace your sid
TWILIO_AUTH_TOKEN = #replace your auth token

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    phone_number = request.form['phone_number'].strip()
    print(f"Received phone number: {phone_number}")  # Debugging statement

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    try:
        number_info = client.lookups.v1.phone_numbers(phone_number).fetch(type=["carrier", "caller-name"])
        result = {
            'number': number_info.phone_number,
            'country': number_info.country_code,
            'carrier': number_info.carrier.get('name', 'Unknown'),
            'line_type': number_info.carrier.get('type', 'Unknown'),
            'caller_name': number_info.caller_name.get('caller_name', 'Not available') if number_info.caller_name else 'Not available',
            'caller_type': number_info.caller_name.get('caller_type', 'Not available') if number_info.caller_name else 'Not available'
        }
    except TwilioRestException as e:
        error_message = e.msg
        if "The requested resource" in error_message:
            error_message = "Number not found. Please check the number and try again."
        result = {'error': error_message}
        print("TwilioRestException occurred:", e)  # Debugging statement
    except Exception as e:
        result = {'error': f"An unexpected error occurred: {str(e)}"}
        print("An unexpected error occurred:", e)  # Debugging statement

    print("Result:", result)  # Debugging statement
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)



