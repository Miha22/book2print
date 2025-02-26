import argparse
from PyPDF2 import PdfReader, PdfWriter

def to_points(x, measure):
    conversion_rate = 72 if measure == "inch" else 28.8
    return x * conversion_rate


def add_margins(input_pdf, output_pdf, primary=0, secondary=0, top=0, bottom=0):
    with open(input_pdf, 'rb') as f:
        reader = PdfReader(f)
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            i = i + 1

            if i % 2 == 0:
                page.mediabox.lower_left = (float(page.mediabox.lower_left[0]) - secondary, float(page.mediabox.lower_left[1]) - bottom)
                page.mediabox.lower_right = (float(page.mediabox.lower_right[0]) + primary, float(page.mediabox.lower_right[1]) - bottom)
                page.mediabox.upper_left = (float(page.mediabox.upper_left[0]) - secondary, float(page.mediabox.upper_left[1]) + top)
                page.mediabox.upper_right = (float(page.mediabox.upper_right[0]) + primary, float(page.mediabox.upper_right[1]) + top)
            else:
                page.mediabox.lower_left = (float(page.mediabox.lower_left[0]) - primary, float(page.mediabox.lower_left[1]) - bottom)
                page.mediabox.lower_right = (float(page.mediabox.lower_right[0]) + secondary, float(page.mediabox.lower_right[1]) - bottom)
                page.mediabox.upper_left = (float(page.mediabox.upper_left[0]) - primary, float(page.mediabox.upper_left[1]) + top)
                page.mediabox.upper_right = (float(page.mediabox.upper_right[0]) + secondary, float(page.mediabox.upper_right[1]) + top)

            writer.add_page(page)

        with open(output_pdf, 'wb') as out:
            writer.write(out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add margins to a PDF file.")
    parser.add_argument('input_pdf', type=str, help="Input PDF file path")
    parser.add_argument('output_pdf', type=str, help="Output PDF file path")
    parser.add_argument('--side_p', type=float, default=0, help="Margin of primary side")
    parser.add_argument('--side_s', type=float, default=0, help="Margin of secondary side")
    parser.add_argument('--top', type=float, default=0, help="Top margin")
    parser.add_argument('--bottom', type=float, default=0, help="Bottom margin")
    parser.add_argument('--measure', type=str, default=0, help="cm or inch")

    args = parser.parse_args()
    measure = args.measure

    add_margins(
        args.input_pdf,
        args.output_pdf,
        to_points(args.side_p, measure),
        to_points(args.side_s, measure),
        to_points(args.top, measure),
        to_points(args.bottom, measure)
    )