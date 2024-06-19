import jinja2
import pdfkit
import pathlib


dir_path = pathlib.Path().resolve()


def create_pdf(html_path, info, css=None):
    template_name = html_path.split("\\")[-1]
    template_path = html_path.replace(template_name, "")

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))
    template = env.get_template(template_name)
    html = template.render(info)

    options = {
        "page-size": "Letter",
        "orientation": "portrait",
        "margin-top": "0.16in",
        "margin-right": "0.1in",
        "margin-bottom": "0.16in",
        "margin-left": "0.1in",
        "encoding": "UTF-8",
        "dpi": 300,
        "no-outline": True,
        "enable-local-file-access": True,
        "images": True,
        "enable-javascript": True,
    }

    

    output_path = f"{dir_path}\\utils\\pdfkit\\output\\output.pdf"
    pdfkit.from_string(
        html, output_path, css=css, options=options
    )


# sample usage
# template_path = f"{dir_path}\\templates\\counterfoil.html"
# info = {
#    "pupil_name": "Pedro Gómez",
#    "course_name": "Python Básico",
#    "date": "2024-06-03",
#    "logo": f"{dir_path}\\public\\images\\icon.png",
#    "headings": ["Item", "Titulo", "Precio"],
#    "data": [
#        {"key": 1, "title": "Item 1", "price": 100.5},
#        {"key": 2, "title": "Item 2", "price": 4.45},
#        {"key": 3, "title": "Item 3", "price": 12.25},
#    ],
# }
# create_pdf(template_path, info, css=f"{dir_path}\\public\\css\\styles.css")
