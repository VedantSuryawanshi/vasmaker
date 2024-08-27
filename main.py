import pandas as pd
import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import json

# Modify variable names in the code
new_csv_file = 'vas.csv'
new_selected_columns = ["FULL NAME", "NEXT SERVICE", "INSURANCE", "PUC", "WORKSHOP", "FUEL", "MAK"]
new_json_template_file = 'manifest.json'
new_env = Environment(loader=FileSystemLoader('.'))
new_template = new_env.get_template('demo.html')
new_output_dir = 'output_html'

# Define the function to extract the first name
def extract_first_name(full_name):
    parts = full_name.split()
    if len(parts) > 0:
        return parts[0]
    else:
        return full_name

# Load CSV data into a DataFrame
df = pd.read_csv(new_csv_file, usecols=new_selected_columns)

# Load the custom JSON template
with open(new_json_template_file, 'r') as json_template:
    json_template_data = json.load(json_template)

# Create a directory to store individual HTML files (if it doesn't exist)
os.makedirs(new_output_dir, exist_ok=True)

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    # Prepare data for the template (one row at a time)
    data = row.to_dict()

    # Set a default value for "Preferred Garage" and update the link
    if pd.isna(data['WORKSHOP']) or data['WORKSHOP'] == '':
        data['WORKSHOP'] = 'WORKSHOP'
        data['Link'] = 'https://cars.mekit.in/bookatgarageform'
    else:
        workshop = data['WORKSHOP']
        # Map workshop to link
        workshop_map = {
            'Express Autocare': 'https://cars.mekit.in/bookatexpressautocare',
            'Yadav Garage': 'https://cars.mekit.in/bookatyadavgarage',
            # Add more mappings as needed
        }
        data['Link'] = workshop_map.get(workshop, 'https://cars.mekit.in/bookatgarageform')

    # Get the current date in the format "DD/MM/YYYY"
    current_date = datetime.now().strftime("%d/%m/%Y")
    data['Last Update'] = current_date

    # Replace missing "FULL NAME" with "Sir"
    if pd.isna(data['FULL NAME']) or data['FULL NAME'] == '':
        data['FULL NAME'] = 'Sir'

    # Extract the first name from the 'FULL NAME' column
    full_name = data['FULL NAME']
    first_name = extract_first_name(full_name)
    # Assign 'first_name' to a 'First Name' field in 'data'
    data['First Name'] = first_name

    # Generate manifest JSON file based on the custom template
    manifest_data = json_template_data.copy()
    manifest_data['start_url'] = f'/{index}'  # Replace the placeholder with the appropriate value

    # Generate JSON file with the data
    json_output = json.dumps(manifest_data, indent=4)
    json_file_name = f'{new_output_dir}/{index}.json'
    with open(json_file_name, 'w') as json_file:
        json_file.write(json_output)

    # Render the HTML using the template and data
    html_output = new_template.render(data=data)

    # Save the generated HTML to a file (one file per row)
    output_file_name = f'{new_output_dir}/{index}.html'
    with open(output_file_name, 'w') as output_file:
        output_file.write(html_output)

    print(f"HTML file {output_file_name} and manifest JSON file {json_file_name} generated successfully!")

print("All HTML and JSON files generated successfully!")
