from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import json
import os

# Modify variable names in the code
template = Environment(loader=FileSystemLoader('.')).get_template('newvasdemo.html')
output_dir = 'output_html'
new_json_template_file = 'manifest.json'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load the custom JSON template
with open(new_json_template_file, 'r') as json_template:
    json_template_data = json.load(json_template)

# Loop through each number from 1200 to 1400
for index in range(1502, 2000):
    # Add manifest file number to the data dictionary
    data = {}
    data['Manifest_File_Number'] = index

    # Add a link to the 'Manifest_Link' in the data dictionary
    data['Manifest_Link'] = f'{index}.json'


    # Render the HTML using the template and data
    html_output = template.render(data=data)

    # Generate manifest JSON file based on the custom template
    manifest_data = json_template_data.copy()
    manifest_data['start_url'] = f'/{index}'  # Replace the placeholder with the appropriate value

    # Generate JSON file with the data
    json_output = json.dumps(manifest_data, indent=4)
    json_file_name = f'{output_dir}/{index}.json'  # Corrected variable name
    with open(json_file_name, 'w') as json_file:
        json_file.write(json_output)

    # Add manifest file number to the data dictionary
    data['Manifest_File_Number'] = index

    # Add a link to the 'Manifest_Link' in the data dictionary
    data['Manifest_Link'] = f'{index}.json'

    # Save the generated HTML to a file (one file per row)
    output_file_name = f'{output_dir}/{index}.html'
    with open(output_file_name, 'w') as output_file:
        output_file.write(html_output)

    print(f"HTML file {output_file_name} and manifest JSON file {json_file_name} generated successfully!")

print("All HTML and JSON files generated successfully!")
