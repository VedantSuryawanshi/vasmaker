import pandas as pd
import os
from jinja2 import Environment, FileSystemLoader
import json

# Modify variable names in the code
new_csv_file = 'luckyvas.csv'
new_selected_columns = ["Name", "Insurance", "PUC", "Model"]
new_json_template_file = 'manifest.json'
new_env = Environment(loader=FileSystemLoader('.'))
new_template = new_env.get_template('newdemo.html')
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
print(df.columns)

# Load the custom JSON template
with open(new_json_template_file, 'r') as json_template:
    json_template_data = json.load(json_template)

# Create a directory to store individual HTML files (if it doesn't exist)
os.makedirs(new_output_dir, exist_ok=True)

# Start the count from 5000
count = 5000

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    # Prepare data for the template (one row at a time)
    data = row.to_dict()

    # Extract the first name from the 'Name' column
    full_name = data['Name']
    first_name = extract_first_name(full_name)

    # Assign 'first_name' to a 'First Name' field in 'data'
    data['First Name'] = first_name

    # Increment the count for each file
    count += 1

    # Generate manifest JSON file based on the custom template
    manifest_data = json_template_data.copy()
    manifest_data['start_url'] = f'/{count}'  # Use the incremented count

    # Generate JSON file with the data
    json_output = json.dumps(manifest_data, indent=4)
    json_file_name = f'{new_output_dir}/{count}.json'
    with open(json_file_name, 'w') as json_file:
        json_file.write(json_output)

    # Add manifest file number to the data dictionary
    data['Manifest_File_Number'] = count

    # Add a link to the 'Manifest_Link' in the data dictionary
    data['Manifest_Link'] = f'{count}.json'

    # Render the HTML using the template and data
    html_output = new_template.render(data=data)

    # Save the generated HTML to a file (one file per row)
    output_file_name = f'{new_output_dir}/{count}.html'
    with open(output_file_name, 'w') as output_file:
        output_file.write(html_output)
    print(f"HTML file {output_file_name} and manifest JSON file {json_file_name} generated successfully!")

print("All HTML and JSON files generated successfully!")
