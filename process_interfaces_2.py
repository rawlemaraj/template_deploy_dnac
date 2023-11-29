#!/usr/bin/env python

import json

# Load the interface data
with open('/tmp/interface_data.json', 'r') as file:
    data = json.load(file)

# Initialize a dictionary to store switch-port mapping and a list for switch-port pairs
switch_port_map = {}
switch_port_pairs = []

# Iterate over the data and aggregate ports
for entry in data:
    for interface in entry.get('dnac_response', {}).get('response', []):
        device_id = interface.get('deviceId')
        port_name = interface.get('portName')
        interface_type = interface.get('interfaceType')  # Assuming this field exists
        status = interface.get('status')  # Assuming this field exists

        # Check for physical interface and status down
        if device_id and port_name and interface_type == 'Physical' and status == 'down':
            if device_id not in switch_port_map:
                switch_port_map[device_id] = []
            if port_name not in switch_port_map[device_id]:
                switch_port_map[device_id].append(port_name)

# Generate switch-port pairs
for device_id, ports in switch_port_map.items():
    for port in ports:
        switch_port_pairs.append({'switch_id': device_id, 'port': port})

# Output the result as JSON
output = {
    'switch_port_map': switch_port_map,
    'switch_port_pairs': switch_port_pairs
}
print(json.dumps(output))
