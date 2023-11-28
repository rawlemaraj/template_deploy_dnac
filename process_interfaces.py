#!/usr/bin/env python

import json

# Load the interface data
with open('/tmp/interface_data.json', 'r') as file:
    data = json.load(file)

# Initialize a dictionary to store switch-port mapping
switch_port_map = {}

# Iterate over the data and aggregate ports
for entry in data:
    for interface in entry.get('dnac_response', {}).get('response', []):
        device_id = interface.get('deviceId')
        port_name = interface.get('portName')
        interface_type = interface.get('interfaceType')  # Assuming this field exists
        status = interface.get('status')  # Assuming this field exists
        description = interface.get('description', '')  # Assuming this field exists

        # Check for physical interface, status down, and specific keywords in description
        if device_id and port_name and interface_type == 'Physical' and status == 'down':
            if 'ATM' in description and 'I' in description:
                if device_id not in switch_port_map:
                    switch_port_map[device_id] = []
                if port_name not in switch_port_map[device_id]:
                    switch_port_map[device_id].append(port_name)

# Output the result as JSON
print(json.dumps(switch_port_map))
