from flask import Flask, request, render_template, jsonify
from markupsafe import Markup
import parse_template


app = Flask(
    __name__,
    static_url_path="",
    static_folder="static",
    template_folder="templates",
)


@app.route("/")
def index():
    template = parse_template.load_json("patient_portal.json")
    form_html = parse_template.parse_json_to_html(template)
    

    #form_html = (
    #    '<form action="/api/submit" method="post">'
    #    + form_html
    #    + "</form>"
    #)

    form_content = Markup(form_html)
    return render_template("dynamic-index.html", form_content=Markup(form_content))


# Endpoint to submits patient data
@app.post("/api/submit")
def submit():
    
    print("hi")

    # return jsonify()


@app.post("/api/retrieve")
def retrieve():
    pass


@app.route('/perform_action', methods=['POST'])
def perform_action():
    data = request.get_json()
    action = data.get('action')

    if action == 'ss':
        result = {'status': 'error', 'message': 'Unknown action'}

    return jsonify(result)