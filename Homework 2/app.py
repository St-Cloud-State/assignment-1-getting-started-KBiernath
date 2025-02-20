from flask import Flask, request, render_template

app = Flask(__name__)

# Store the applications in memory
applications = {}
application_counter = 1

# Valid statuses
VALID_STATUSES = ['received', 'processing', 'accepted', 'rejected']

@app.route('/')
def index():
    # Just show the main page with no messages
    return render_template('index.html')

@app.route('/accept_application', methods=['POST'])
def accept_application():
    global application_counter

    name = request.form.get('name')
    zipcode = request.form.get('zipcode')

    if not name or not zipcode:
        return render_template('index.html', 
            accept_msg="Error: Name and ZIP code are required.")

    # Save the application
    applications[application_counter] = {
        'name': name,
        'zipcode': zipcode,
        'status': 'received'
    }

    message = f"Application accepted. Your application number is {application_counter}."
    application_counter += 1

    # Return the same index.html, with accept_msg passed in
    return render_template('index.html', accept_msg=message)

@app.route('/check_status', methods=['POST'])
def check_status():
    try:
        app_number = int(request.form.get('application_number'))
    except ValueError:
        return render_template('index.html', 
            check_msg="Error: Invalid application number.")

    if app_number not in applications:
        return render_template('index.html', 
            check_msg=f"Application #{app_number} not found.")

    status = applications[app_number]['status']
    return render_template('index.html', 
        check_msg=f"Application #{app_number} status: {status}")

@app.route('/change_status', methods=['POST'])
def change_status():
    try:
        app_number = int(request.form.get('application_number'))
    except ValueError:
        return render_template('index.html', 
            change_msg="Error: Invalid application number.")

    new_status = request.form.get('new_status')

    if app_number not in applications:
        return render_template('index.html', 
            change_msg=f"Application #{app_number} not found.")

    if new_status not in VALID_STATUSES:
        return render_template('index.html', 
            change_msg=f"Error: Valid statuses are {VALID_STATUSES}.")

    applications[app_number]['status'] = new_status
    return render_template('index.html', 
        change_msg=f"Status for Application #{app_number} changed to '{new_status}'.")

if __name__ == '__main__':
    app.run(debug=True)
