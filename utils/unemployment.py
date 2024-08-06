from pathlib import Path
import fitz  # PyMuPDF
from models.companies import Companies
from database.config import session

def form_unemployment_pdf_generator():
    company = session.query(Companies).filter(Companies.id == 1).first()

    def data_entry():
        return {
            'ein_first_part': '38',
            'ein_second_part': '1237056',
            'company_name': company.name,
        }
    
    rute = Path(__file__).parent.absolute()
    document_dir = rute.parent / 'output_files'
    source_file_name = 'unemployment_plantilla.pdf'
    output_file_name = 'unemployment.pdf'

    data_entry = data_entry()


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
                    if field.field_name == 'txtNombrePatrono':
                        field.field_value = data_entry['company_name']
                        field.update()
        # Save the updated PDF
        doc.save(document_dir / output_file_name, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        doc.close()

    return document_dir / output_file_name
