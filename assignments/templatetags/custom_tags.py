from django import template

register = template.Library()

@register.simple_tag
def render_quiz_answer_form(form):
    output = ""
    for field in form:
        output += f"<div>"
        output += f"<p class='text-xl font-semibold'>{field.label_tag}</p>"
        output += f"{field[0]} {field[1]}"  # Render the radio button and hidden ID
        output += f"</div>"
    return output
