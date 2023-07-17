# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    new_formated_dates=[]
    for date in old_dates:
        new_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d %b %Y') 
        new_formated_dates.append(new_date)
    return new_formated_dates

def date_range(start, n):
    date_range_objects = []
    if not isinstance(start, str):
        raise TypeError
    elif not isinstance(n, int):
        raise TypeError
    else:
        start_date = datetime.strptime(start, '%Y-%m-%d')
        for i in range(n):
            date_range_objects.append(start_date+timedelta(days=+i))
    return date_range_objects


def add_date_range(values, start_date):
    expected_dates = date_range(start_date, len(values))
    expected = list(zip(expected_dates, values))
    return expected

def fees_report(infile, outfile):
    with open(infile) as fi:
        rows=[]
        input_dict = DictReader(fi)
        for item in input_dict:
            row={}
            num_of_days=(datetime.strptime(item['date_returned'],'%m/%d/%Y')- datetime.strptime(item['date_due'],'%m/%d/%Y')).days
            if(num_of_days>0):
                row["patron_id"]=item['patron_id']
                row["late_fees"]=round(num_of_days*0.25, 2)
            else:
                row["patron_id"]=item['patron_id']
                row["late_fees"]=0.00
            rows.append(row)
        aggregated_output = {}
        for row in rows :
            key = (row['patron_id'])
            aggregated_output[key] = aggregated_output.get(key, 0) + row['late_fees']
        fee = [{'patron_id': key, 'late_fees': value} for key, value in aggregated_output.items()]
        for ele in fee:
            for k,v in ele.items():
                if k == "late_fees":
                    if len(str(v).split('.')[-1]) != 2:
                        ele[k] = str(v)+'0'

    with open(outfile,"w", newline="") as file:
        cols = ['patron_id', 'late_fees']
        writer = DictWriter(file, fieldnames=cols)
        writer.writeheader()
        writer.writerows(fee)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
