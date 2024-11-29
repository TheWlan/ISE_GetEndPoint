import requests
import csv
import urllib3
from creds import USERNAME, PASSWORD, ISE_IP  # Import credentials from creds.py

def get_endpoints():
    # Suppress SSL warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # Define the API endpoint for getting endpoints, updated to use port 443
    endpoint_url = f"https://{ISE_IP}:443/ers/config/endpoint"

    # Define headers for the API request
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        # Make a GET request to the endpoint URL
        response = requests.get(endpoint_url, auth=(USERNAME, PASSWORD), headers=headers, verify=False)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            # Extract endpoint information
            endpoints = data.get('SearchResult', {}).get('resources', [])
            return endpoints
        else:
            # If the request was unsuccessful, print the error message
            print(f"Failed to retrieve endpoints. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_endpoint_group(endpoint_id):
    # Define the API endpoint for getting endpoint details, updated to use port 443
    endpoint_url = f"https://{ISE_IP}:443/ers/config/endpoint/{endpoint_id}"

    # Define headers for the API request
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        # Make a GET request to the endpoint URL
        response = requests.get(endpoint_url, auth=(USERNAME, PASSWORD), headers=headers, verify=False)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            # Extract endpoint group information
            endpoint_group = data.get('ERSEndPoint', {}).get('groupId', 'N/A')
            return endpoint_group
        else:
            # If the request was unsuccessful, print the error message
            print(f"Failed to retrieve endpoint group for endpoint {endpoint_id}. Status code: {response.status_code}")
            return 'N/A'
    except Exception as e:
        print(f"An error occurred while retrieving endpoint group for endpoint {endpoint_id}: {e}")
        return 'N/A'

def get_endpoint_group_name(endpoint_group_id):
    # Define the API endpoint for getting endpoint group details, updated to use port 443
    endpoint_url = f"https://{ISE_IP}:443/ers/config/endpointgroup/{endpoint_group_id}"

    # Define headers for the API request
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        # Make a GET request to the endpoint URL
        response = requests.get(endpoint_url, auth=(USERNAME, PASSWORD), headers=headers, verify=False)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            # Extract endpoint group name
            endpoint_group_name = data.get('EndPointGroup', {}).get('name', 'N/A')
            return endpoint_group_name
        else:
            # If the request was unsuccessful, print the error message
            print(f"Failed to retrieve endpoint group with ID {endpoint_group_id}. Status code: {response.status_code}")
            return 'N/A'
    except Exception as e:
        print(f"An error occurred while retrieving endpoint group with ID {endpoint_group_id}: {e}")
        return 'N/A'

def read_group_names_from_csv(filename):
    group_names = set()
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            group_names.add(row['Endpoint Group'])
    return group_names

def main():
    # Read group names from CSV
    allowed_groups = read_group_names_from_csv('Groups.csv')

    # Call the function to get endpoints
    endpoints = get_endpoints()
    if endpoints:
        with open('filtered_endpoint_data.csv', mode='w', newline='') as file:
            fieldnames = ['MAC', 'Endpoint Group']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for endpoint in endpoints:
                endpoint_id = endpoint['id']
                endpoint_name = endpoint['name']
                endpoint_group_id = get_endpoint_group(endpoint_id)
                endpoint_group_name = get_endpoint_group_name(endpoint_group_id)
                if endpoint_group_name in allowed_groups:
                    writer.writerow({'MAC': endpoint_name, 'Endpoint Group': endpoint_group_name})
    else:
        print("Failed to retrieve endpoints.")

if __name__ == "__main__":
    main()
