import csv

def generate_insurance_message(name, model, expiry):
    # Extracting the first name from the full name
    first_name = name.split()[0]
    return f"Hello {first_name} sir, insurance for your {model} expires soon on {expiry}. Please send me your latest policy so that I can send you some quote options."

def process_csv(input_file, output_file):
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        sentences = []
        for row in reader:
            name = row.get('NAME', '')
            model = row.get('MODEL', '')
            expiry = row.get('Expiry', '')

            if name and model and expiry:
                message = generate_insurance_message(name, model, expiry)
                sentences.append(message)

    with open(output_file, 'w') as textfile:
        for sentence in sentences:
            textfile.write(sentence + '\n')
            
    print(f"Sentences generated and saved to '{output_file}'.")
    print(f"Number of sentences generated: {len(sentences)}")

if __name__ == "__main__":
    input_csv_file = 'ins.csv'
    output_text_file = 'output_sentences.txt'

    process_csv(input_csv_file, output_text_file)
