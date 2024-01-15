import pandas as pd
import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import json

# Modify variable names in the code
new_csv_file = 'vas.csv'
new_selected_columns = ["FULL NAME", "NEXT SERVICE", "INSURANCE", "PUC", "WORKSHOP", "FUEL","MAK"]
new_json_template_file = 'manifest.json'
new_env = Environment(loader=FileSystemLoader('.'))
new_template = new_env.get_template('demo.html')
new_output_dir = 'output_html'
new_fuel_cost_per_type = {
    "Petrol": 125,
    "Diesel": 150,
    "CNG": 125,
    "Electric": 0
}
new_mileage = 12
new_fuel_cost_per_liter = 105

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

# Convert "Fuel Avg run/month" to numeric (float) with a default of 500 if missing or non-numeric
df["FUEL"] = pd.to_numeric(df["FUEL"], errors="coerce").fillna(500).astype(int)

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
    elif data['WORKSHOP'] == 'Express Autocare':
        data['Link'] = 'https://cars.mekit.in/bookatexpressautocare'
    elif data['WORKSHOP'] == 'Yadav Garage':
        data['Link'] = 'https://cars.mekit.in/bookatyadavgarage'
    elif data['WORKSHOP'] == 'Wash and More':
        data['Link'] = 'https://cars.mekit.in/bookatwashandmore'
    elif data['WORKSHOP'] == 'Aher Auto':
        data['Link'] = 'https://cars.mekit.in/bookataherauto'
    elif data['WORKSHOP'] == 'Auto Trust':
        data['Link'] = 'https://cars.mekit.in/bookatautotrust'
    elif data['WORKSHOP'] == 'Landmark Renault':
        data['Link'] = 'https://cars.mekit.in/bookatlandmarkrenault'
    elif data['WORKSHOP'] == 'Landmark Thane':
        data['Link'] = 'https://cars.mekit.in/bookatlandmarkthane'
    elif data['WORKSHOP'] == 'Mannu Auto':
        data['Link'] = 'https://cars.mekit.in/bookatmannuauto'
    elif data['WORKSHOP'] == 'Modi Hyundai':
        data['Link'] = 'https://cars.mekit.in/bookatmodihyundai'
    elif data['WORKSHOP'] == 'Regent Honda':
        data['Link'] = 'https://cars.mekit.in/bookatregenthonda'
    elif data['WORKSHOP'] == 'Satyam Ford':
        data['Link'] = 'https://cars.mekit.in/bookatsatyamford'
    elif data['WORKSHOP'] == 'Sudarshan Tata':
        data['Link'] = 'https://cars.mekit.in/bookatsudarshantata'
    elif data['WORKSHOP'] == 'Suzuki Thane':
        data['Link'] = 'https://cars.mekit.in/bookatsuzukithane'
    elif data['WORKSHOP'] == 'VW Thane':
        data['Link'] = 'https://cars.mekit.in/bookatvwthane'
    elif data['WORKSHOP'] == 'Millennium Toyota':
        data['Link'] = 'https://cars.mekit.in/bookatmillenniumtoyota'
    elif data['WORKSHOP'] == 'Dealership':
        data['Link'] = 'https://cars.mekit.in/bookatdealership'
    elif data['WORKSHOP'] == 'Workshop':
        data['Link'] = 'https://cars.mekit.in/bookatgarageform'



    # Calculate the monthly fuel cost based on "FUEL"
    fuel_avg_run_per_month = data['FUEL']
    if pd.isna(fuel_avg_run_per_month):
            fuel_avg_run_per_month = 500  # Set a default value of 500

    monthly_fuel_cost = (fuel_avg_run_per_month / new_mileage) * new_fuel_cost_per_liter
    
    # Set a default value of 500 if it's less than or equal to 0
    if fuel_avg_run_per_month <= 0:
        fuel_avg_run_per_month = 500

    # Get the current date in the format "DD/MM/YYYY"
    current_date = datetime.now().strftime("%d/%m/%Y") 
    data['Last Update'] = current_date

    # Add the calculated monthly fuel cost to the data dictionary
    data['MAK'] = monthly_fuel_cost
    
    # Get the "Fuel Type" from the data
    fuel_type = data.get('FUEL', 'Petrol')  # Default to Petrol if Fuel Type is missing

    # Calculate the monthly fuel cost based on "FUEL"
    fuel_avg_run_per_month = data['FUEL']
    if pd.isna(fuel_avg_run_per_month):
        fuel_avg_run_per_month = 500  # Set a default value of 500

    # Calculate the monthly PUC renewal cost based on the "Fuel Type"
    puc_renewal_cost = new_fuel_cost_per_type.get(fuel_type, 125)  # Default to 125 for unknown fuel types

    # Add the PUC renewal cost and "Fuel Type" to the data dictionary
    data['PUC Renewal Cost'] = puc_renewal_cost
    data['Fuel Type'] = fuel_type
    
    print("Fuel Type:", fuel_type)
    print("PUC Renewal Cost:", puc_renewal_cost)

    # Replace missing "FULL NAME" with "Sir"
    if pd.isna(data['FULL NAME']) or data['FULL NAME'] == '':
        data['FULL NAME'] = 'Sir'

    # Calculate the fuel cost for 4 months
    fuel_cost_for_4_months = monthly_fuel_cost * 4
    data['Fuel Cost for 4 Months'] = fuel_cost_for_4_months

    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
    # Extract the first name from the 'FULL NAME' column
     data = row.to_dict()
     full_name = data['FULL NAME']
     first_name = extract_first_name(full_name)

    # Now, you can use 'first_name' in your code as needed

    # Example: Assign 'first_name' to a 'First Name' field in 'new_data'
    data['First Name'] = first_name

    # Add 'First Name' as a new column in your DataFrame
    df['First Name'] = df['FULL NAME'].apply(extract_first_name)
    # Generate manifest JSON file based on the custom template
    manifest_data = json_template_data.copy()
    manifest_data['start_url'] = f'/{index}'  # Replace the placeholder with the appropriate value

    # Generate JSON file with the data
    json_output = json.dumps(manifest_data, indent=4)
    json_file_name = f'{new_output_dir}/{index}.json'
    with open(json_file_name, 'w') as json_file:
        json_file.write(json_output)

    # Add manifest file number to the data dictionary
    data['Manifest_File_Number'] = index

    # Add a link to the 'Manifest_Link' in the data dictionary
    data['Manifest_Link'] = f'{index}.json'

    # Render the HTML using the template and data
    html_output = new_template.render(data=data)

    # Save the generated HTML to a file (one file per row)
    output_file_name = f'{new_output_dir}/{index}.html'
    with open(output_file_name, 'w') as output_file:
        output_file.write(html_output)
    print(f"HTML file {output_file_name} and manifest JSON file {json_file_name} generated successfully!")

print("All HTML and JSON files generated successfully!")



