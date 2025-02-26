from itertools import islice
import PyPDF2
from PyPDF2.pdf import PageObject
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTChar
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import math
from datetime import datetime
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from io import BytesIO

a4_width_pt = 296 * 72 / 25.4
a4_height_pt = 211 * 72 / 25.4

def format_timedelta(td):
    days, remainder = divmod(td.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = td.microseconds // 1000
    
    formatted_output = ""
    if days > 0:
        formatted_output += f"{int(days)} days, "
    if hours > 0:
        formatted_output += f"{int(hours)} hours, "
    if minutes > 0:
        formatted_output += f"{int(minutes)} minutes, "
    if seconds > 0 or (seconds == 0 and not milliseconds):
        formatted_output += f"{int(seconds)}"
    if milliseconds:
        formatted_output += f".{milliseconds}"
    formatted_output += " seconds"

    return formatted_output

def process_page(page, side, margin_bleed_side, margin_side):#side 0 - left, 1 - right
    page.mediaBox = page.trimBox    
    margin_bleed_side_pt = (margin_bleed_side * 72 / 25.4)
    margin_side_pt = (margin_side * 72 / 25.4)
    x_len_pt = (a4_width_pt / 2) - margin_bleed_side_pt - margin_side_pt
    
    page_width = float(page.cropBox.getWidth())
    page_height = float(page.cropBox.getHeight())
    
    scale = x_len_pt / page_width
    y_len_pt = page_height * scale
    margin_tb_pt = (a4_height_pt - y_len_pt) / 2
    page.scaleBy(scale)
    
    translation_x = float(-page.mediaBox.lowerLeft[0])
    translation_y = float(-page.mediaBox.lowerLeft[1])
    
    page.cropBox = page.mediaBox
    page.artBox = page.mediaBox
    page.bleedBox = page.mediaBox
    
    return (page, (margin_side_pt + translation_x, margin_tb_pt + translation_y) if side == 0 else (a4_width_pt / 2 + margin_bleed_side_pt + translation_x, margin_tb_pt + translation_y))
    
def create_line_page(p_left_num: str = "", p_right_num: str = "", font_size = 7):
    packet = BytesIO()
    width, height = landscape(A4)
    c = canvas.Canvas(packet, pagesize=landscape(A4))
    c.setLineWidth(1)
    c.setStrokeColorRGB(0, 0, 0)
    c.setDash(1, 2)
    c.line(width/2, 0, width/2, height) #drawing line in the middle of page

    c.setFont("Times-Roman", font_size)

    y_position = 14 + font_size / 2
    c.drawCentredString(width / 4, y_position, p_left_num)
    c.drawCentredString(width / 4 + width / 2, y_position, p_right_num)
    
    c.save()
    packet.seek(0)
    lined_pdf = PyPDF2.PdfFileReader(packet)
    
    return lined_pdf.getPage(0)

def combine_pages(page1, t1, page2, t2):
    if page1 == None and page2 == None:
        return None
    new_page = PageObject.createBlankPage(width=a4_width_pt, height=a4_height_pt)
    if page1 != None:
        new_page.mergeTranslatedPage(page1, t1[0], t1[1])
    if page2 != None:
        new_page.mergeTranslatedPage(page2, t2[0], t2[1])
    
    return new_page
    

def combine_pages_landscape_with_margins(input_pdf_path, output_pdf_path,
                                        margin_bleed_side, margin_side):
    with open(input_pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        pdf_writer = PyPDF2.PdfFileWriter()
        
        num_pages = pdf_reader.numPages
        #num_pages = 5
        num_a4_in_stack = 6
        num_a4_pages = math.ceil(num_pages / 4)
        num_stacks = math.ceil(num_a4_pages / num_a4_in_stack)
        
        s_i = 0
        #counter = 0
        iterations = num_a4_in_stack * 2
        p_i = 0
        start_time = datetime.now()
        while s_i != num_stacks:                  
            start_time = datetime.now() 
            print(f"#4 processing stack: {s_i + 1}/{num_stacks}")              
            num_pages_stack = iterations * 2
            
            if p_i == iterations:  
                s_i = s_i + 1                 
                p_i = 0
                with open(output_pdf_path+f".{s_i}.pdf", 'wb') as output_file:
                    pdf_writer.write(output_file)
                    output_file.close()
                    if s_i == num_stacks:
                        print("Done.")
                        break
                pdf_writer = PyPDF2.PdfFileWriter()
                end_time = datetime.now()
                time_difference = (end_time - start_time) * (num_stacks - s_i)
                f_dt = format_timedelta(time_difference)
                print(f"[DONE]#4 processing stack: {s_i + 1}/{num_stacks}")  
                print(f"\tEstimated time remaining: {f_dt}\n") 
                    
            page1 = None
            obj1 = None
            page2 = None
            obj2 = None
            p_left_num = ""
            p_right_num = ""
            
            if p_i + num_pages_stack * s_i < num_pages:
                page1 = pdf_reader.getPage(p_i + num_pages_stack * s_i)
                obj1 = process_page(page1, 1 if p_i % 2 == 0 else 0, margin_bleed_side, margin_side)
                if p_i % 2 == 0:
                    p_right_num = str(p_i + num_pages_stack * s_i + 1)
                else:
                    p_left_num = str(p_i + num_pages_stack * s_i + 1)
            else:
                p_i = iterations
                continue
             
            if num_pages_stack - 1 + (num_pages_stack * s_i) - p_i < num_pages:    
                page2 = pdf_reader.getPage(num_pages_stack - 1 + (num_pages_stack * s_i) - p_i)
                obj2 = process_page(page2, 0 if p_i % 2 == 0 else 1, margin_bleed_side, margin_side)
                if p_i % 2 == 1:
                    p_right_num = str(num_pages_stack - 1 + (num_pages_stack * s_i) - p_i + 1)
                else:
                    p_left_num = str(num_pages_stack - 1 + (num_pages_stack * s_i) - p_i + 1)

            a4_combine = combine_pages(obj1[0] if obj1 != None else None, 
                                       obj1[1] if obj1 != None else None, 
                                       obj2[0] if obj2 != None else None, 
                                       obj2[1] if obj2 != None else None
                                       )
            if a4_combine != None:
                p = create_line_page(p_left_num, p_right_num, 9)
                a4_combine.mergePage(p)
                pdf_writer.addPage(a4_combine)
            p_i = p_i + 1

def get_dimensions(page, update, interpreter, device):
    interpreter.process_page(page)
    layout = device.get_result()

    #initial extreme values for coordinates
    # x_min = 77
    # x_max = 535
    # y_min = 80
    # y_max = 718
    x_min = update[0]
    x_max = update[1]
    y_min = update[2]
    y_max = update[3]
    
    for element in layout:
        if isinstance(element, LTTextBox) or isinstance(element, LTTextLine):
            x, y, x1, y1 = element.bbox
            x_min = min(x_min, x) if x_min > x and x_min - x < (x_min * 0.15) else x_min
            y_min = min(y_min, y) if y_min > y and y_min - y < (y_min * 0.15) else y_min
            x_max = max(x_max, x1)
            y_max = max(y_max, y1)

    return x_min, x_max, y_min, y_max

def get_text_area_dimensions(p_from, len, pdf_path, page_number = -1):
    with open(pdf_path, 'rb') as file:
        t = (77, 535, 80, 718)
        #specific page
        if len == -1:
            len = len - p_from
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for i, page in islice(enumerate(PDFPage.create_pages(PDFDocument(PDFParser(file)))), p_from, len):
            # if i < p_from or p_from + len - 1 < i:
            #     continue
            print(f"#1 processing: {i}/{len + p_from - 1}")
            #if page_number == -1:
            t = get_dimensions(page, t, interpreter, device)
                #tuples_list.append(t)
            # else: 
            #     if i == page_number:
            #         return get_dimensions(page)
        file.close()
        
        return t


def crop_all_pages(p_from, p_len, tuple, pdf_path, output_path, specified_page = -1):    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        pdf_writer = PyPDF2.PdfFileWriter()
        #tuple = (0, 0, 0, 0)
        
        # if(specified_page != -1):
        #     # Get the specific page to crop
        #     tuple = get_text_area_dimensions(pdf_path, specified_page, tuple)
        #     page = pdf_reader.getPage(specified_page)
            
        #     # Set the crop box based on provided coordinates
        #     page.cropBox.lowerLeft = (tuple[0], tuple[2])
        #     page.cropBox.upperRight = (tuple[1], tuple[3])
            
        #     # Add the cropped page to the new PDF writer object
        #     pdf_writer.addPage(page)
        #     with open("/Users/veteranmac/Desktop/test.pdf", 'wb') as output_file:
        #         pdf_writer.write(output_file)
        #     return
        # Loop through each page
        for i, page in enumerate(pdf_reader.pages):
            if i < p_from or p_from + p_len - 1 < i:
                continue 
            
            #print(f"processing: {round(float(page_num / pdf_reader.numPages * 100), 2)}%")
            print(f"#2 processing: {i}/{p_len + p_from - 1}")
            #getting specific page to crop
            #tuple = get_text_area_dimensions(pdf_path, page_num, tuple)
            #page = pdf_reader.getPage(i + p_from)
            #tuple = tuple_list[i - p_from]
            #setting crop box based on provided coordinates
            page.cropBox.lowerLeft = (tuple[0], tuple[2])
            page.cropBox.upperRight = (tuple[1], tuple[3])
            
            #adding cropped page to new pdf writer object
            pdf_writer.addPage(page)
        
        # Save the cropped PDF
        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)


book = 'linear-algebra-mathematica.pdf'
output_pdf_path = "cropped-{book}"
input_pdf = output_pdf_path
output_pdf = "stacks/stack.pdf"
start_page_i = 15
len = 668

tuple = get_text_area_dimensions(start_page_i, len, book)
crop_all_pages(start_page_i, len, tuple, book, output_pdf_path)
combine_pages_landscape_with_margins(input_pdf, output_pdf, 
                                     margin_bleed_side = 15, margin_side = 5)