from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import uuid
import os
from dotenv import load_dotenv
from markupsafe import Markup
import parse_template  # Assuming this is your module for loading and parsing templates

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn

@app.route("/")
def index():
    # Render dynamic form based on the template JSON
    template = parse_template.load_json("template.json")
    form_html = parse_template.parse_json_to_html(template)
    form_html = (
        '<form action="/api/submit" method="post" enctype="multipart/form-data">'
        + form_html
        + '<button type="submit" class="btn btn-primary">Submit</button>'
        + "</form>"
    )
    form_content = Markup(form_html)
    return render_template("dynamic-index.html", form_content=form_content)

@app.post("/api/submit")
def submit():
    # Extract form data using IDs from template.json
    patient_id = request.form.get('patient_id')
    chief_complaint = request.form.get('chiefComplaint')
    history_of_present_illness = request.form.get('HPI')
    past_medical_history = request.form.get('pastMedicalHistory')
    surgical_history = request.form.get('surgicalHistory')
    family_medical_history = request.form.get('familyHistory')
    social_history = request.form.get('socialHistory')
    allergies = request.form.get('allergies')

    height = request.form.get('height')
    weight = request.form.get('weight')
    bmi = request.form.get('bmi')
    blood_pressure = request.form.get('bloodPressure')
    temperature = request.form.get('temperature')
    pulse = request.form.get('pulse')
    o2_oximeter = request.form.get('oxygen')

    constitutional = request.form.get('constitutionalPhysical')
    ent = request.form.get('entPhysical')
    respiratory = request.form.get('respiratoryPhysical')
    cardiovascular = request.form.get('cardiovascularPhysical')
    caloric = request.form.get('caloricPhysical')
    skin = request.form.get('skinPhysical')
    extremities = request.form.get('extremitiesPhysical')
    neurological = request.form.get('neurologicalPhysical')

    assessment_notes = request.form.get('assessmentNotes')
    plan_details = request.form.get('planDetails')
    follow_up = request.form.get('followUp')

    # Handle file upload for test results
    test_results = None
    if 'testResults' in request.files:
        file = request.files['testResults']
        if file and file.filename != '':
            test_results = file.read()

    # Generate a unique UUID and convert it to a string
    note_id = str(uuid.uuid4())

    # Insert data into the database
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Use execute with tuple to safely insert data
        cur.execute('''
            INSERT INTO soap_notes (
                id, patient_id, chief_complaint, history_of_present_illness, past_medical_history,
                surgical_history, family_medical_history, social_history, allergies,
                height, weight, bmi, blood_pressure, temperature, pulse, o2_oximeter,
                constitutional, ent, respiratory, cardiovascular, caloric, skin, extremities, neurological,
                assessment_notes, plan_details, follow_up, test_results
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (note_id, patient_id, chief_complaint, history_of_present_illness, past_medical_history,
              surgical_history, family_medical_history, social_history, allergies,
              height, weight, bmi, blood_pressure, temperature, pulse, o2_oximeter,
              constitutional, ent, respiratory, cardiovascular, caloric, skin, extremities, neurological,
              assessment_notes, plan_details, follow_up, psycopg2.Binary(test_results) if test_results else None))

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        flash(f"An error occurred: {e}")
        return redirect(url_for('index'))

    # Flash a success message
    flash('Thank you, the form is submitted successfully!')

    # Redirect to a thank you page
    return redirect(url_for('thank_you'))

@app.route("/thank_you")
def thank_you():
    return render_template("thank_you.html")

if __name__ == "__main__":
    app.run(debug=True)
