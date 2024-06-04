import csv
import datetime

from puc import generate_puc_message

def generate_service_message(name, model, expiry, workshop):
    first_name = name.split()[0]
    formatted_expiry = expiry.strftime("%d %b %Y")  # Format expiry date
    workshop_message = f"at {workshop}" if workshop else "at your preferred garage"
    return f"🔔 Service for your {model} is due on {formatted_expiry}\n\nHi {first_name} sir, let me know, and I'll book an appointment {workshop_message} and get your car’s service done, while I save your time and money."

def process_puc_csv(input_file, output_file):
    service_messages = []

    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            name = row.get('NAME', '')
            model = row.get('MODEL', '')  
            expiry_str = row.get('Expiry', '')

            if name and model and expiry_str:
                try:
                    expiry = datetime.datetime.strptime(expiry_str, "%d %b %Y").date()
                    service_message = generate_service_message(name, model, expiry, workshop=None)
                    service_messages.append(service_message)
                except ValueError as e:
                    print(f"Error processing row: {row}, {e}")

    if not service_messages:
        print("No valid data found in the input CSV file.")
        return

    with open(output_file, 'w') as textfile:
        for message in service_messages:
            textfile.write(message + '\n')

    print(f"Service messages generated and saved to '{output_file}'.")
    print(f"Number of service messages generated: {len(service_messages)}")

# Example usage:
process_puc_csv("service.csv", "servicedue.txt")
