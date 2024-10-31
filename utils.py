import json
from database import VMMService
from datetime import datetime


class SoapNoteTemplate:
    def __init__(self, db: VMMService, soapnote_id: str):
        self.db = db
        self.soapnote_id = soapnote_id

    def parse_json_to_html(self, data, level=1):
        html_parts = []

        if isinstance(data, dict):
            fields = data.get("fields", [])
            for field in fields:
                label = field.get("label", "")
                field_id = field.get("id", "")
                field_type = field.get("type", "")
                input_type = field.get("inputType", "")
                placeholder = field.get("placeholder", "")

                if field_type == "group":
                    # Header tags based on level
                    html_parts.append(f'<div id="{field_id}" class="ms-4">')
                    html_parts.append(f'<h{level} class="mb-2">{label}</h{level}>')
                    # Recursively process nested fields
                    html_parts.append(self.parse_json_to_html(field, level + 1))
                    html_parts.append("</div>")

                else:
                    html_parts.append('<div class="input-group">')
                    html_parts.append(f'<span class="input-group-text">{label}</span>')

                    if input_type == "textarea":
                        html_parts.append(
                            f'<{input_type} id="{field_id}" name="{field_id}" type="{field_type}" class="form-control" aria-label="{label}" placeholder="{placeholder}">{self.soapnote_content.get(field_id, "")}</{input_type}>'
                        )
                    elif input_type == "input":
                        html_parts.append(
                            f'<{input_type} id="{field_id}" name="{field_id}" type="{field_type}" class="form-control" aria-label="{label}" placeholder="{placeholder}" value="{self.soapnote_content.get(field_id, "")}">'
                        )

                    html_parts.append("</div>")
                    html_parts.append("<br>")

        return "\n".join(html_parts)

    async def get_form(self, template_file_path: str):
        with open(template_file_path, "r") as file:
            template = json.load(file)

        self.soapnote_content = await self.get_soapnote_content()

        form_html = self.parse_json_to_html(template)

        return form_html

    async def get_soapnote_content(self):
        soapnote_entry = await self.db.search_unique("soapnote", id=self.soapnote_id)

        return soapnote_entry.noteContent

    async def update_soapnote_content(self, field_data):
        await self.db.update_soapnote(self.soapnote_id, field_data)


class PatientPortal:
    def __init__(self, db: VMMService):
        self.db = db

    async def get_patients(self, patient_name):
        found_patients = await self.db.search_name("patient", patient_name)

        return found_patients


class AddRecords:
    def __init__(self, db: VMMService):
        self.db = db

    async def prase_objects(record_objects: list) -> list[str]:
        return [str([obj.name, obj.id]) for obj in record_objects]

    async def list_doctors(self):
        doctors = await self.db.list_all("doctor")
        return doctors

    async def list_patients(self, doctor=""):
        if doctor == "":
            patients = await self.db.list_all("patient")
        else:
            patients = await self.db.list_patients(doctor.id)

        return patients


class Appointments:
    def __init__(self, db: VMMService):
        self.db = db

    async def get_doctor_id(self, doctor_name):
        doctors = await self.db.search_name("doctor", doctor_name)
        if doctors:
            return (doctors[0], doctors[0].id)
        return None

    async def get_patientid_by_name(self, patient_name):  # for server.py
        patient = await self.db.search_name("patient", patient_name)
        if patient:
            return (patient[0], patient[0].id)
        return None

    async def get_patient_name_by_id(self, patient_id):  # for js
        patient = await self.db.search_unique("patient", id=patient_id)
        if patient:
            return patient.name
        return None

    async def push_appointment_date(self, doctor_id, patient_id, content, start, end):
        await self.db.add_appointment(doctor_id, patient_id, content, start, end)

    async def get_events_by_doctor_id(self, doctor_id):
        print("util retrieval")
        return await self.db.get_events_by_doctor_id(doctor_id)
