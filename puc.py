import csv
from datetime import datetime

def generate_puc_message(name, model, expiry):
    days_to_expiry = (expiry - datetime.now().date()).days
    formatted_expiry = expiry.strftime("%d %b %y")
    return f"{name} - 🔔 {model}'s PUC is going to expire in {days_to_expiry} days on {formatted_expiry}."

def process_puc_csv(input_file, output_file):
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        puc_messages = []
        for row in reader:
            name = row.get('NAME', '')
            model = row.get('Model', '')
            expiry_str = row.get('Expiry', '')

            if name and model and expiry_str:
                try:
                    expiry = datetime.strptime(expiry_str, "%d %b %Y").date()
                    puc_message = generate_puc_message(name, model, expiry)
                    puc_messages.append(puc_message)
                except ValueError as e:
                    print(f"Error processing row: {row}, {e}")

    if not puc_messages:
        print("No valid data found in the PUC CSV file.")
        return

    with open(output_file, 'w') as textfile:
        for message in puc_messages:
            textfile.write(message + '\n')

    print(f"PUC messages generated and saved to '{output_file}'.")
    print(f"Number of PUC messages generated: {len(puc_messages)}")

if __name__ == "__main__":
    input_puc_csv_file = 'puc.csv'  # Replace with the actual PUC CSV file name
    output_puc_text_file = 'output_puc_messages.txt'

    process_puc_csv(input_puc_csv_file, output_puc_text_file)
