import os
import numpy as np
import pandas as pd
import re
import sys
import textract

min_chars_in_file = 10
output_file = 'pdf_search_output.csv'

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

pdf_dir = sys.argv[1]

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

print("\n%s out of %s files were successfully parsed." % (total_parsed, total))

avg = sum(lengths) / len(lengths)
print("Average length: %s chars." % avg)

results['Total'] = results.iloc[:,2:].sum(axis = 1)
results = results.sort_values(by = 'Total', ascending = False)

print("Found an average of %s hits per document." % np.mean(results['Total']))
print("%s out of %s had a hit." % (len(np.where(results['Total'] > 0)[0]), total))

results.to_csv(output_file, index = None, header = True)
print("Results saved to %s" % output_file)

colsums = results.sum(axis = 0)[2:]
print("Overall Hit Count:")
print(colsums)

# import code; code.interact(local=dict(globals(), **locals()))
