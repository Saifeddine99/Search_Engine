import csv
csv_file_path="heart_failure_clinical_records_dataset.csv"

def process_boolean(value):
    return value == '1'

count=0
with open(csv_file_path, 'r', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for idx, row in enumerate(csv_reader, start=1):
        diabetes= process_boolean(row['diabetes'])
        anaemia= process_boolean(row['anaemia'])
        smoking= process_boolean(row['smoking'])
        high_blood_pressure= process_boolean(row['high_blood_pressure'])
        if diabetes and smoking==False:
            count+=1

print(count)
