import pandas as pd
import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import json

# Load CSV data into a DataFrame
csv_file = 'data.csv'
# Specify the columns you want to use
selected_columns = ["Full name", "Next service", "Insurance", "PUC", "Workshop", "Avg run/month", "Fuel type"]
df = pd.read_csv(csv_file, usecols=selected_columns)

# Load the custom JSON template
json_template_file = 'manifest.json'
with open(json_template_file, 'r') as json_template:
    json_template_data = json.load(json_template)

# Load the Jinja2 template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('demo.html')

# Convert "Fuel Avg run/month" to numeric (float) with a default of 500 if missing or non-numeric
df["Avg run/month"] = pd.to_numeric(df["Avg run/month"], errors="coerce").fillna(500).astype(int)

# Create a directory to store individual HTML files (if it doesn't exist)
output_dir = 'output_html'
os.makedirs(output_dir, exist_ok=True)

# Fuel cost based on fuel type (PUC renewal cost)
fuel_cost_per_type = {
    "Petrol": 125,
    "Diesel": 150,
    "CNG": 125,
    "Electric": 0  # Assuming electric vehicles have no PUC renewal cost
}

# Fuel mileage (km per liter)
mileage = 12

# Fuel cost per liter (assuming 105 INR per liter)
fuel_cost_per_liter = 105

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    # Prepare data for the template (one row at a time)
    data = row.to_dict()

    # Set a default value for "Preferred Garage" and update the link
    if pd.isna(data['Workshop']) or data['Workshop'] == '':
        data['Workshop'] = 'Workshop'
        data['Link'] = 'https://cars.mekit.in/bookatgarageform'
    elif data['Workshop'] == 'Express Autocare':
        data['Link'] = 'https://cars.mekit.in/bookatexpressautocare'
    elif data['Workshop'] == 'Yadav Garage':
        data['Link'] = 'https://cars.mekit.in/bookatyadavgarage'
    elif data['Workshop'] == 'Wash and More':
        data['Link'] = 'https://cars.mekit.in/bookatwashandmore'
    elif data['Workshop'] == 'Aher Auto':
        data['Link'] = 'https://cars.mekit.in/bookataherauto'
    elif data['Workshop'] == 'Auto Trust':
        data['Link'] = 'https://cars.mekit.in/bookatautotrust'
    elif data['Workshop'] == 'Landmark Renault':
        data['Link'] = 'https://cars.mekit.in/bookatlandmarkrenault'
    elif data['Workshop'] == 'Landmark Thane':
        data['Link'] = 'https://cars.mekit.in/bookatlandmarkthane'
    elif data['Workshop'] == 'Mannu Auto':
        data['Link'] = 'https://cars.mekit.in/bookatmannuauto'
    elif data['Workshop'] == 'Modi Hyundai':
        data['Link'] = 'https://cars.mekit.in/bookatmodihyundai'
    elif data['Workshop'] == 'Regent Honda':
        data['Link'] = 'https://cars.mekit.in/bookatregenthonda'
    elif data['Workshop'] == 'Satyam Ford':
        data['Link'] = 'https://cars.mekit.in/bookatsatyamford'
    elif data['Workshop'] == 'Sudarshan Tata':
        data['Link'] = 'https://cars.mekit.in/bookatsudarshantata'
    elif data['Workshop'] == 'Suzuki Thane':
        data['Link'] = 'https://cars.mekit.in/bookatsuzukithane'
    elif data['Workshop'] == 'VW Thane':
        data['Link'] = 'https://cars.mekit.in/bookatvwthane'
    elif data['Workshop'] == 'Millennium Toyota':
        data['Link'] = 'https://cars.mekit.in/bookatmillenniumtoyota'
    elif data['Workshop'] == 'Dealership':
        data['Link'] = 'https://cars.mekit.in/bookatdealership'

    # Calculate the monthly fuel cost based on "Fuel Avg run/month"
    fuel_avg_run_per_month = data['Avg run/month']
    if pd.isna(fuel_avg_run_per_month):
            fuel_avg_run_per_month = 500  # Set a default value of 500

    monthly_fuel_cost = (fuel_avg_run_per_month / mileage) * fuel_cost_per_liter
    
    # Set a default value of 500 if it's less than or equal to 0
    if fuel_avg_run_per_month <= 0:
        fuel_avg_run_per_month = 500
    
    # Get the current date in the format "DD/MM/YYYY"
    current_date = datetime.now().strftime("%d/%m/%Y")
    data['Last Update'] = current_date

    # Add the calculated monthly fuel cost to the data dictionary
    data['Monthly Fuel Cost'] = monthly_fuel_cost

    # Get the "Fuel Type" from the data
    fuel_type = data.get('Fuel Type', 'Petrol')  # Default to Petrol if Fuel Type is missing
    puc_renewal_cost = fuel_cost_per_type.get(fuel_type, 125)  # Default to 125 for unknown fuel types

    # Add the PUC renewal cost and "Fuel Type" to the data dictionary
    data['PUC Renewal Cost'] = puc_renewal_cost
    data['Fuel Type'] = fuel_type  # Add or overwrite the value
    
    # Replace missing "Full name" with "Sir"
    if pd.isna(data['Full name']) or data['Full name'] == '':
        data['Full name'] = 'Sir'

    # Calculate the fuel cost for 4 months
    fuel_cost_for_4_months = monthly_fuel_cost * 4
    data['Fuel Cost for 4 Months'] = fuel_cost_for_4_months
    

    # Generate manifest JSON file based on the custom template
    manifest_data = json_template_data.copy()
    manifest_data['start_url'] = f'/{index}'  # Replace the placeholder with the appropriate value

    # Generate JSON file with the data
    json_output = json.dumps(manifest_data, indent=4)
    json_file_name = f'output_json/{index}.json'
    with open(json_file_name, 'w') as json_file:
        json_file.write(json_output)

    # Add manifest file number to the data dictionary
    data['Manifest_File_Number'] = index

    # Render the HTML using the template and data
    html_output = template.render(data=data)

    # Save the generated HTML to a file (one file per row)
    output_file_name = f'output_html/{index}.html'
    with open(output_file_name, 'w') as output_file:
        output_file.write(html_output)

    print(f"HTML file {output_file_name} and manifest JSON file {json_file_name} generated successfully!")

print("All HTML and JSON files generated successfully!")