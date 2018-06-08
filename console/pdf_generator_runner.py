import sys
from traffic.pdf.pdf_generator import generate_pdf_report, valid_pdf_install

if not valid_pdf_install():
    sys.stderr.write("Report Lab is not installed, cannot generate pdf report.")
    exit(-1)

directory = sys.argv[1]

if generate_pdf_report(directory):
    exit(0)
else:
    exit(-1)
