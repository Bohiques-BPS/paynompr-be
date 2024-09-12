from pathlib import Path
import fitz  # PyMuPDF
from models.companies import Companies
from database.config import session
from models.queries.queryFormUnemployment import queryFormUnemployment


def form_unemployment_pdf_generator():
    company = session.query(Companies).filter(Companies.id == 1).first()

    rute = Path(__file__).parent.absolute()
    document_dir = rute.parent / 'output_files'
    source_file_name = 'template/unemployment_plantilla.pdf'
    output_file_name = 'unemployment.pdf'

    # data_entry = data_entry()

    data_entry = queryFormUnemployment(company.id)


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
                        # print(field.field_name, '-', data_entry[field.field_name])
                        field.field_value = data_entry[field.field_name]
                        field.update()
                    # if field.field_name == '4155960009':
                    #     field.field_value = data_entry['ein_first_part']
                    #     field.update()
        # Save the updated PDF
        doc.save(document_dir / output_file_name, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        doc.close()

    return document_dir / output_file_name
