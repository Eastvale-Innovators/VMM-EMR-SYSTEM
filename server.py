from quart import Quart, request, render_template, jsonify
from markupsafe import Markup
import utils
from database import VMMService
from datetime import datetime
import json

app = Quart(
    __name__,
    static_url_path="",
    static_folder="static",
    template_folder="templates",
)

db = VMMService()


@app.template_global("get_year")
def get_year():
    return datetime.today().year


@app.before_serving
async def startup():
    await db.connect()


@app.after_serving
async def shutdown():
    await db.disconnect()


@app.route("/")
async def index():
    return await render_template("index.html")


@app.route("/soap-notes/<uuid:soapnote_id>", methods=["GET", "POST"])
async def soap_notes(soapnote_id):
    soapnote_helper = utils.SoapNoteTemplate(db, str(soapnote_id))

    if request.method == "POST":
        form_data = await request.form
        await soapnote_helper.update_soapnote_content(form_data)

        return "OK"

    else:
        form_html = await soapnote_helper.get_form("template.json")

        form_content = Markup(form_html)
        return await render_template(
            "soap-notes.html", form_content=Markup(form_content)
        )


@app.post("/add-records/patient")
async def add_patient():
    form_data = await request.form
    try:
        await db.add_patient(
            doctor=form_data.get("doctor", ""),
            name=form_data.get("name", ""),
            sex=form_data.get("sex", ""),
            dob=form_data.get("dob", ""),
        )

        return "OK"

    except Exception as e:
        return e


@app.route("/add-records")
async def add_records():
    record_helper = utils.AddRecords(db)
    doctor_list = await record_helper.list_doctors()
    print(*doctor_list)
    return await render_template("add-records.html", doctor_list=doctor_list)


@app.route("/patient-portal", methods=["GET", "POST"])
async def patient_portal():
    if request.method == "POST":
        patient_name = (await request.form).get("name-query", "")

        portal_helper = utils.PatientPortal(db)
        found_patients = await portal_helper.get_patients(patient_name)

        patient_soapnotes = {
            patient.id: (await db.search_many("soapnote", patientId=patient.id))[0]
            for patient in found_patients
        }

        return await render_template(
            "patient-portal.html",
            patient_list=found_patients,
            soapnote_list=patient_soapnotes,
        )

    return await render_template("patient-portal.html")


@app.route("/appointments", methods=["GET", "POST"])
async def appointments_index():

    if request.method == "POST":
        appointment_data = await request.get_json()
        title = appointment_data['title']
        start = appointment_data['start']
        end = appointment_data['end']
        doctor = appointment_data['doctor']
        patient = appointment_data['patient']

        print(f"New appointment: {title}, {start} - {end}, Doctor: {doctor}, Patient: {patient}")
        appointments_helper = utils.Appointments(db)

        # Format date
        try:
            start = datetime.fromisoformat(start).isoformat() + 'Z'
            end = datetime.fromisoformat(end).isoformat() + 'Z'
        except ValueError as e:
            print(f"Date formatting error: {e}")
            return jsonify({"success": False, "message": "Error in rendering date!\nError Code 32A"}), 400

        doctor_return = await appointments_helper.get_doctor_id(doctor)
        patient_return = await appointments_helper.get_patientid_by_name(patient)

        print("doctor")
        print(doctor_return)
        print("patient")
        print(patient_return)

        if doctor_return and patient_return:
            doctor_obj = doctor_return[0]
            doctor_id = doctor_return[1]

            patient_obj = patient_return[0]
            patient_id = patient_return[1]

            showMessage = "Successfully added appointment date!"
            await appointments_helper.push_appointment_date(doctor_id, patient_id, title, start, end)
            return await render_template("appointments.html")
        else:
            print("Appointments didn't go through!")
            return jsonify({"success": False, "message": "Error in finding doctor and patient!\nError Code: 32B"}), 400
    
    return await render_template("appointments.html")

    
@app.route("/appointments/doctor=<string:doctor>", methods=["GET"])
async def get_doctor_events(doctor):
    appointments_helper = utils.Appointments(db)

    doctor_return = await appointments_helper.get_doctor_id(doctor)
    doctor_id = doctor_return[1]

    events = await appointments_helper.get_events_by_doctor_id(doctor_id)

    print(events)

    if events:
        return events
    else:
        return jsonify({"success": False, "message": "No events found for this doctor."}), 404

@app.route("/appointments/patient=<string:patientID>", methods=["GET"])
async def get_patient_by_id(patientID):
    appointments_helper = utils.Appointments(db)

    print("hi")

    id_return = await appointments_helper.get_patient_name_by_id(patientID)

    print(id_return)
    
    if id_return:
        return id_return
    else:
        return None
    

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)