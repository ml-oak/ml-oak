import json
import xmltodict

# Specify the path to the XML file
xml_file_path = 'data.xml'

# Read the XML content and parse it to a dictionary
with open(xml_file_path, 'r') as xml_file:
    xml_content = xml_file.read()
    json_data = json.dumps(xmltodict.parse(xml_content), indent=4)

# Specify the path for the output JSON file
json_file_path = 'output.json'

# Write the JSON data to a JSON file
with open(json_file_path, 'w') as json_file:
    json_file.write(json_data)

print(f'XML converted to JSON and saved to {json_file_path}')
