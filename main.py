import csv

csv_file = open('pequanock_data.csv', 'r')

csv_reader = csv.DictReader(csv_file)

"""
    - List of Outputs from program that are derived from grouping by address, and creating list of results
    
    - similar to the following sql
        SELECT <OUTPUTS BELOW> FROM donations_table GROUP BY contributor_street_1
    
    - List Format: each element of the list is a tuple of the following format
        (output_column_name, input_column_name)
            -> input_column_name = name of column in input table 
            -> output_column_name = name of aggregated column in output table
"""
outputs = [
    ('names', 'contributor_name'),
    ('occupations', 'contributor_occupation'),
    ('committee', 'committee_name')
]

funding_map = {}
count_map = {}
outputs_lists = [{} for i in range(len(outputs))]
for row in csv_reader:
    address = row["contributor_street_1"]

    funding_map.setdefault(address, 0)
    contribution = float(row["contribution_receipt_amount"])
    funding_map[address] += contribution

    count_map.setdefault(address, 0)
    count_map[address] += 1

    for i, output_def in enumerate(outputs):
        output_name, col_name = output_def
        value = row[col_name]
        outputs_lists[i].setdefault(address, [])
        if value not in outputs_lists[i][address]:
            outputs_lists[i][address] += [value]

results = []
for address in funding_map:
    count = count_map[address]
    funding = funding_map[address]
    outputs_row = [" / ".join(outputs_map[address]) for outputs_map in outputs_lists]
    results += [(address, funding, count, *outputs_row)]

results = sorted(results, key=lambda x: x[1])
row_format_str = '{},{:.2f},{}' + ',"{}"'*len(outputs) + '\n'
f = open('USR_results.csv', 'w')
outputs_rows_header = ','.join(x[0] for x in outputs)
f.write(f'address, total_funding, count, {outputs_rows_header}\n')
for row in results:
    f.write(row_format_str.format(*row))
f.close()
