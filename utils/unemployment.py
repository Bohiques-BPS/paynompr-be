from pathlib import Path
import fitz  # PyMuPDF
from database.config import session
from models.queries.queryFormUnemployment import queryFormUnemployment


def form_unemployment_pdf_generator():

    rute = Path(__file__).parent.absolute()
    document_dir = rute.parent / 'output_files'
    source_file_name = 'template/planilla_form_unemployees_part_1.pdf'
    output_file_name = 'unemployment_0.pdf'

    data_entry = []

    try:
        data_entry = queryFormUnemployment(1, 2024, 3)
    except Exception as e:
        print(f"An error occurred obtain data: {e}")
        return None


    try:
        # Open the source PDF
        doc = fitz.open(document_dir / source_file_name)
    except Exception as e:
        print(f"Failed to open document: {e}")
        return None

    try:
        for page_number in range(len(doc)):
            page = doc[page_number]
            for field in page.widgets():
                if field.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                    if field.field_name in data_entry:
                        field.field_value = data_entry[field.field_name]
                        field.update()
        # Save the updated PDF
        doc.save(document_dir / output_file_name, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        doc.close()

    return document_dir / output_file_name
