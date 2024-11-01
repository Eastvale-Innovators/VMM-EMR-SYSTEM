from quart import Quart, request, render_template
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


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
