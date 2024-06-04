import csv

def generate_insurance_message(name, model, expiry, workshop):
    # Extracting the first name from the full name
    first_name = name.split()[0]

    # Checking if workshop is None and adjusting the message accordingly
    workshop_message = f"at {workshop}" if workshop else "at your preferred garage"

    return f"🔔 Service for your {model} is due on {expiry}\n \n Hi {first_name} sir, let me know, and I'll book an appointment {workshop_message} and get your car’s service done, while I save your time and money."

def process_csv(input_file, output_file):
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        sentences = []
        for row in reader:
            name = row.get('NAME', '')
            model = row.get('MODEL', '')
            expiry = row.get('Expiry', '')
            workshop = row.get('Workshop', '')  

            if name and model and expiry:
                message = generate_insurance_message(name, model, expiry, workshop)
                sentences.append(message)

    with open(output_file, 'w') as textfile:
        for sentence in sentences:
            textfile.write(sentence + '\n')
            
    print(f"Sentences generated and saved to '{output_file}'.")
    print(f"Number of sentences generated: {len(sentences)}")

if __name__ == "__main__":
    input_csv_file = 'service.csv'
    output_text_file = 'servicedue.txt'

    process_csv(input_csv_file, output_text_file)
