import pandas as pd
import glob
import os
import csv

def txt_to_csv(input_file, output_file):
    with open(input_file, 'r') as infile:
        stripped = (line.strip() for line in infile)
        lines = (line.split(",") for line in stripped if line)
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(lines)

os.chdir('C:\\Users\\mykell.frank\\Dropbox (FlexShopper)\\Finance Shared Folder\\Mykell F\\Central Payments Attribution 07-24-24')
path = r'C:\Users\mykell.frank\Dropbox (FlexShopper)\Finance Shared Folder\Mykell F\CDR Data MTD - 07-01 to 07-23'

for filename in os.listdir(path):
    if filename.endswith('.txt'):
        input_file = os.path.join(path, filename)
        output_file = os.path.join(path, filename.replace('.txt', '.csv'))
        txt_to_csv(input_file, output_file)

all_files = glob.glob(os.path.join(path, "*.csv"))

call_data = pd.concat((pd.read_csv(f, engine='python', on_bad_lines='skip', encoding="unicode_escape") for f in all_files), ignore_index=True)
phone_mapping = pd.read_csv('User by Number.csv')
transactions = pd.read_csv('Transactions MTD 07-21-2024.csv', parse_dates=['transaction_date'])

call_data = call_data.rename(columns={'Contact Target':'phone_number'})
call_data_combined = call_data.merge(right=phone_mapping, how='left', on="phone_number")
successful_transfers = call_data_combined[call_data_combined['Operator Transfer Successful'] == 1]

combined_data = transactions.merge(right=successful_transfers, how='left', on='user_id')
combined_data['daysSincePayment'] = (pd.to_datetime(combined_data['transaction_date'], errors='coerce') - pd.to_datetime(combined_data['Date'], errors='coerce')).dt.days

contacted_payments = combined_data[(combined_data['daysSincePayment'] >= 0) & (combined_data['daysSincePayment'] <= 2)]
contacted_payments.to_csv('Collections Central Attributed Payments 07-21-24.csv', index=False)