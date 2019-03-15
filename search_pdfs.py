import os
import pandas as pd
import re
import sys
import textract

pdf_dir = sys.argv[1]

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
search_terms = [s.lower() for s in search_terms]

min_chars_in_file = 10

files = [f for f in os.listdir(pdf_dir) if os.path.isfile(pdf_dir + f)]
files = [f for f in files if f.endswith(('.pdf', '.PDF'))]

total = len(files)
total_parsed = 0
count = 0
lengths = []
results = pd.DataFrame(columns = ['filename', 'doc_length'] + search_terms)
print("Processing %s files..." % total)
for filename in files:
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

        row_data = {'filename': filename, 'doc_length': length}
        for term in search_terms:
            text = str(text)
            occurences = 0
            if term in text:
                occurences = len(text.split(term)) - 1
            row_data[term] = occurences
        results = results.append(row_data, ignore_index = True)
        success = True

    if success: total_parsed += 1

print("%s out of %s files were successfully parsed." % (total_parsed, total))

avg = sum(lengths) / len(lengths)
print("Average length: %s chars." % avg)

results['Total'] = results.iloc[:,2:].sum(axis = 1)
results = results.sort_values(by = 'Total', ascending = False)
results.to_csv('pdf_search_output.csv', index = None, header = True)

# import code; code.interact(local=dict(globals(), **locals()))
