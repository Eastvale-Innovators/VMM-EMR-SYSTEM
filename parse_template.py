import json

def load_json(filename: str) -> dict:
    with open(filename, "r") as file:
        template = json.load(file)

    return template


def parse_json_to_html(data, level=1):
    html_parts = []

    if isinstance(data, dict):
        fields = data.get("fields", [])
        for field in fields:
            label = field.get("label", "")
            field_id = field.get("id", "")
            field_type = field.get("type", "")
            input_type = field.get("inputType", "")
            placeholder = field.get("placeholder", "")
            options = field.get("options", [])
            actionName = field.get("actionname", "")
            table_columns = field.get("columns", [])
            table_rows = field.get("rows", [])

            if field_type == "group":
                html_parts.append(f'<div id="{field_id}" class="p-4">')
                html_parts.append(f"<h{level}>{label}</h{level}>")
                html_parts.append(parse_json_to_html(field, level + 1)) #keep adding all its sub components
                html_parts.append("</div>")
                html_parts.append("<hr>")
            elif field_type == "divider":
                html_parts.append('<hr>')
            elif field_type == "semititle":
                html_parts.append(f'<div id="{field_id}" class="p-1">')
                html_parts.append(f"<h3>{label}</h4>")
                html_parts.append("</div>")
            elif field_type == "caption":
                html_parts.append(f'<div id="{field_id}" class="p-1">')
                html_parts.append(f"<p>{label}</p>")
                html_parts.append("</div>")
            elif input_type == "textarea":
                html_parts.append('<div class="input-group mb-3">')
                html_parts.append(f'<span class="input-group-text">{label}</span>')
                html_parts.append(
                    f'<textarea id="{field_id}" class="form-control" aria-label="{label}" placeholder="{placeholder}"></textarea>'
                )
                html_parts.append("</div>")
                html_parts.append("<br>")

            elif input_type == "input":
                html_parts.append('<div class="input-group mb-3">')
                html_parts.append(f'<span class="input-group-text">{label}</span>')
                html_parts.append(
                    f'<input type="{field.get("inputType", "text")}" id="{field_id}" class="form-control" aria-label="{label}" placeholder="{placeholder}">'
                )
                html_parts.append("</div>")
                html_parts.append("<br>")

            elif input_type == "checkbox":
                html_parts.append('<div class="form-check">')
                html_parts.append(
                    f'<input class="form-check-input" type="checkbox" id="{field_id}">'
                )
                html_parts.append(f'<label class="form-check-label" for="{field_id}">{label}</label>')
                html_parts.append("</div>")
                html_parts.append("<br>")

            elif input_type == "radio":
                for option in options:
                    option_id = option.get("id", "")
                    option_label = option.get("label", "")
                    html_parts.append('<div class="form-check">')
                    html_parts.append(
                        f'<input class="form-check-input" type="radio" name="{field_id}" id="{option_id}">'
                    )
                    html_parts.append(f'<label class="form-check-label" for="{option_id}">{option_label}</label>')
                    html_parts.append("</div>")
                html_parts.append("<br>")

            elif input_type == "select":
                html_parts.append('<div class="input-group mb-3">')
                html_parts.append(f'<label class="input-group-text" for="{field_id}">{label}</label>')
                html_parts.append(f'<select class="form-select" id="{field_id}">')
                for option in options:
                    option_value = option.get("value", "")
                    option_label = option.get("label", "")
                    html_parts.append(f'<option value="{option_value}">{option_label}</option>')
                html_parts.append("</select>")
                html_parts.append("</div>")
                html_parts.append("<br>")

            elif input_type == "date":
                html_parts.append('<div class="input-group mb-3">')
                html_parts.append(f'<span class="input-group-text">{label}</span>')
                html_parts.append(
                    f'<input type="date" id="{field_id}" class="form-control" aria-label="{label}">'
                )
                html_parts.append("</div>")
                html_parts.append("<br>")

            elif input_type == "number":
                html_parts.append('<div class="input-group mb-3">')
                html_parts.append(f'<span class="input-group-text">{label}</span>')
                html_parts.append(
                    f'<input type="number" id="{field_id}" class="form-control" aria-label="{label}" placeholder="{placeholder}">'
                )
                html_parts.append("</div>")
                html_parts.append("<br>")

            elif field_type == "button":
                html_parts.append(f'<button class="btn btn-secondary" id="{field_id}" data-action="{actionName}">{label}</button>')
                html_parts.append("<br>")

            elif field_type == "table":
                html_parts.append(f'<table class="table table-striped table-hover sortable" id = "{field_id}">')
                # Table headers
                html_parts.append("<thead><tr>")
                for column in table_columns:
                    html_parts.append(f'<th>{column.get("label", "")}</th>')
                html_parts.append("</tr></thead>")
                
                # Table rows
                html_parts.append("<tbody>")
                for row in table_rows:
                    html_parts.append("<tr>")
                    for column in table_columns:
                        col_id = column.get("id", "")
                        html_parts.append(f'<td>{row.get(col_id, "")}</td>')
                    html_parts.append("</tr>")
                html_parts.append("</tbody>")
                html_parts.append("</table>")

    return "\n".join(html_parts)


if __name__ == "__main__":
    template = load_json("template.json")
    html_output = parse_json_to_html(template)

    print(html_output)
