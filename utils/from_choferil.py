from pathlib import Path
import fitz  # PyMuPDF
from models.companies import Companies
from models.queries.queryFormChoferil import queryFormChoferil

def form_choferil_pdf_generator(company_id, year, period):


    rute = Path(__file__).parent.absolute()
    document_dir = rute.parent / 'output_files'
    source_file_name = 'choferil_plantilla.pdf'
    output_file_name = 'choferil.pdf'

    data_entry = queryFormChoferil(company_id, year, period)


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
