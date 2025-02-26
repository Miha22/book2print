# PDF Stacking and Book Assembly Script
This script is useful for anyone looking to print large PDFs in a structured way for physical bookbinding.
## Overview
These scripts are designed to process and organize PDFs into structured entities called **stacks**, which contain a certain number of pages. These stacks are later **stitched together** in a specific arrangement to assemble a printable book. The script ensures that pages are correctly split, oriented, and formatted for an optimized print layout.

## Features
- **Splitting PDFs into Stacks**: The script intelligently divides a given PDF into multiple stacks, each with a predefined number of pages.
- **Page Formatting & Scaling**: Adjusts pages to fit within an A4 landscape layout while maintaining appropriate margins and scaling.
- **Correct Page Ordering**: Organizes pages in a way that allows seamless assembly into a booklet format.
- **Crop Detection**: Analyzes the PDF content to detect text regions and crops pages accordingly.
- **Automatic Page Numbering**: Adds visual indicators to help align pages correctly during the bookbinding process.
- **Processing Time Estimation**: Provides estimated completion time based on the number of pages and stacks being processed.

## How It Works
1. **Extract & Crop Pages**:
   - The script reads an input PDF and determines the appropriate text regions.
   - It crops all pages based on detected dimensions.
2. **Organizing Pages into Stacks**:
   - The script calculates the number of **A4-sized stacks** required.
   - It assigns pages to stacks while ensuring proper order for booklet printing.
3. **Combining Pages into a Landscape Format**:
   - Each A4 landscape page is filled with two PDF pages, ensuring an optimal layout.
   - A separator line is added to distinguish pages.
4. **Generating the Final Output**:
   - The script outputs separate stack files, ready for printing and assembly.

## Requirements
To run this script, ensure you have the loaded requirements.txt ```pip install -r /path/to/requirements.txt```

## Usage
I'll write full guide later, begin looking at **crop.py** and examples down below the script
```python
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

```
1. If you have **.epub** then use module epub2pdf.py **(will be uploaded later)**, __convert to pdf first__ 
2. Supply number of pages the PDF book has and the starting page (make it odd)
3. Adjust margins. I recommend keep number of stacks as it is in code **10** since most of A4 pages are quite thick, so it will be easier to bend your book.  

The output will consist of **multiple stack files** *stack.1.pdf, stack.2.pdf...stack.25.pdf, stack.26.pdf*, each representing a portion of the final book. Once printed, these stacks can be bound (to be stitched) together into a complete makeshift book.

## Notes & Comments
- Ensure the input PDF is properly formatted before processing.
- The script assumes an A4 landscape format; adjustments may be required for other sizes.
- Processing time may vary depending on the number of pages.

I have tested and created own makeshift book consisted of 668 pages, For 668 pages the logic will split PDF book into 668 / 4 / 10 + 1 stacks (17 stacks). The pages in stack will be organized in proper order for stitching i.e. (beginning page 1 on right side landscape) page 1 with last page on the same sheet to the left, then on the other side of that same sheet page 2 with pre-last page of the book. 
All caveats took into account. I personally printed the book and stitched it. **I would recommend to increase the marging on each page towards the center of sheet, to be easy on turning the page over.**