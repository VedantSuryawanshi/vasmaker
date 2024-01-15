import pandas as pd
import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import json

# Load CSV data into a DataFrame
csv_file = 'lucky.csv'
# Specify the columns you want to use
selected_columns = ["Name", "Insurance", "PUC"]
df = pd.read_csv(csv_file, usecols=selected_columns)

# Load the custom JSON template
json_template_file = 'manifest.json'
with open(json_template_file, 'r') as json_template:
    json_template_data = json.load(json_template)

# Load the Jinja2 template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('demo.html')


# Create a directory to store individual HTML files (if it doesn't exist)
output_dir = 'output_html'
os.makedirs(output_dir, exist_ok=True)

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    # Prepare data for the template (one row at a time)
    data = row.to_dict()

    
    # Get the current date in the format "DD/MM/YYYY"
    current_date = datetime.now().strftime("%d/%m/%Y")
    data['Last Update'] = current_date
    
    # Replace missing "Full name" with "Sir"
    if pd.isna(data['Name']) or data['Name'] == '':
        data['Name'] = 'Sir'


     # Generate manifest JSON file based on the custom template
    manifest_data = json_template_data.copy()
    manifest_data['start_url'] = f'/{index}'  # Replace the placeholder with the appropriate value

    # Generate JSON file with the data
    json_output = json.dumps(manifest_data, indent=4)
    json_file_name = f'output_json/{index}.json'
    with open(json_file_name, 'w') as json_file:
        json_file.write(json_output)

    # Set the output HTML file name based on the 'index'
    output_file_name = f'output_html/{index}.html'

    # Update the manifest file name in the HTML template to match the 'index'
    html_output = template.render(data=data, index=index, manifest_file_name=f'{index}.json')

    with open(output_file_name, 'w') as output_file:
        output_file.write(html_output)

    print(f"HTML file {output_file_name} and manifest JSON file {json_file_name} generated successfully!")

print("All HTML and JSON files generated successfully!")