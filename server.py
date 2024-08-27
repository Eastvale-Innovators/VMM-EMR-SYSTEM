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
    template = parse_template.load_json("template.json")
    form_html = parse_template.parse_json_to_html(template)
    form_html = (
        '<form action="/api/submit" method="post">'
        + form_html
        + '<button type="submit" class="btn btn-primary">Submit</button>'
        + "</form>"
    )
    form_content = Markup(form_html)
    return render_template("dynamic-index.html", form_content=Markup(form_content))


# Endpoint to submits patient data
@app.post("/api/submit")
def submit():
    
    print(request.form)
    
    # patient_data = request.get_json()

    # for key, value in patient_data.items():
    #     print(f"{key}: {value}")

    # return jsonify()


@app.post("/api/retrieve")
def retrieve():
    pass

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    return render_template('index.html')
