import os
import pandas
import re
import textract

pdf_dir = '/Users/eisner/data/Plans_In_Effect/'

# Dashes are removed so co-op should be coop:
search_terms = [
    'affordable housing',
    'seniors housing',
    'social housing',
    'low income housing',
    'affordability',
    'subsidized housing',
    'inclusive housing',
    'public housing',
    'coop housing',
    'cooperative housing'
]

min_chars_in_file = 10

files = [f for f in os.listdir(pdf_dir) if os.path.isfile(pdf_dir + f)]
files = [f for f in files if f.endswith(('.pdf', '.PDF'))]

total = len(files)
total_parsed = 0
count = 0
lengths = []
print("Processing %s files..." % total)
for filename in files[:10]:
    count += 1
    if count % 25 == 0: print("Finished %s" % count)
    filepath = pdf_dir + filename
    text = textract.process(filepath) #method='tesseract', language='eng')
    text = text.strip()

    success = False
    length = len(text)
    lengths = lengths + [length]
    if (length >= min_chars_in_file):
        text = text.lower()
        text = text.replace(b"\n", b" ")
        text = text.replace(b"-", b"") # Remove dashes for easier searching
        text = re.sub(b' +', b' ', text)


        import code; code.interact(local=dict(globals(), **locals()))
        success = True

    if success: total_parsed += 1

print("%s out of %s files were successfully parsed." % (total_parsed, total))

avg = sum(lengths) / len(lengths)
print("Average length: %s chars." % avg)
import code; code.interact(local=dict(globals(), **locals()))
