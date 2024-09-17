from pathlib import Path
import fitz  # PyMuPDF
from database.config import session
from models.queries.queryFormUnemployment import queryFormUnemployment


def form_unemployment_pdf_generator(company_id, year, period):

    try:
        rute = Path(__file__).parent.absolute()
        document_dir = rute.parent / 'output_files'
        source_file_name = 'template/plantilla_unemployees_tmp.pdf'
        # source_file_name_2 = 'template/planilla_form_unemployees_part_2.pdf'
        output_file_name = 'unemployment.pdf'

        data_entry = []

        try:
            data_entry = queryFormUnemployment(company_id, year, period)
            employees = data_entry['employees']

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

            doc.save(document_dir / output_file_name, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)

            # Open the source PDF
            # for index, listEmployees in enumerate(employees, start=1):
            #     doc2 = fitz.open(document_dir / source_file_name_2)
            #     output_file_name_2 = f'unemployment_{index}.pdf'
            #     for field in doc2[0].widgets():
            #         if field.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
            #             for employee in listEmployees:
            #                 if field.field_name in employee:
            #                     field.field_value = employee[field.field_name]
            #                     field.update()
            #             if field.field_name in data_entry:
            #                 field.field_value = data_entry[field.field_name]
            #                 field.update()
            #             if field.field_name == 'text_total_wages':
            #                 field.field_value = str(len(listEmployees))
            #                 field.update()
            #             if field.field_name == 'text_total_employers' and len(employees) == index:
            #                 field.field_value = data_entry['text_total_wages_a']
            #                 field.update()


                # doc2.save(document_dir / output_file_name_2, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)

            # Save the updated PDF

            # Merge all PDFs
    #         print('Merging all PDFs')
    #         print(output_file_name_array)
    #         doc3 = fitz.open()
    #         for file in output_file_name_array:
    #             doc3.insert_file(file)
    #
    #         doc3.save(document_dir / merge_file_name, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            doc.close()


        return document_dir / output_file_name
    except Exception as e:
        print(f"An error occurred: {e}")
        return None