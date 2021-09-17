import csv
from datetime import datetime, timedelta
import math

from package import Package, create_package_hash


# Read distances.csv and generate a list
def get_distance_data():
    with open('data/distances.csv') as file:
        distance_list = list(csv.reader(file, delimiter=','))
    return distance_list


# Read addresses.csv and generate a list
def get_address_data():
    with open('data/addresses.csv') as file:
        address_list = list(csv.reader(file, delimiter=','))
    return address_list


# Get the distance between two addresses
def distance_between_addresses(address1, address2):
    distance_list = get_distance_data()
    address_list = get_address_data()
    address1_index = None
    address2_index = None

    # Find the index of the first address in addresses.csv
    for first_address in address_list:
        if first_address[2] == address1:
            address1_index = int(first_address[0])

    # Find the index of the second address in addresses.csv
    for second_address in address_list:
        if second_address[2] == address2:
            address2_index = int(second_address[0])

    # Use the index of the first and second address to find the distance in distances.csv
    if distance_list[address1_index][address2_index] == '':
        return distance_list[address2_index][address1_index]
    else:
        return distance_list[address1_index][address2_index]


# Calculate the next closest stop to the current address based on a list of packages on a truck
def find_next_stop(address1, truck_packages):
    shortest_distance = 50.0
    next_stop = ''
    package_data = create_package_hash()
    packages_on_truck = []

    # Get all data for each package on the truck and create a list containing the complete data for each package.
    for package_id in truck_packages:
        package_object = format(package_data.search(package_id)).split(',')
        packages_on_truck.append(package_object)

    # Loop through the list of packages on the truck and find the package with the next closest address
    for package in packages_on_truck:
        address2 = package[1]
        distance = float(distance_between_addresses(address1, address2))

        # The next closest address becomes the next stop
        if distance < shortest_distance:
            shortest_distance = distance
            next_stop = str(address2)

    return next_stop


# Greedy algorithm to calculate the locally optimized route from a list of packages on a truck
# Ref: C950 - Webinar-2 - Getting Greedy, who moved my data
def find_optimized_route(truck_packages):
    optimized_route = [1]  # List to hold address indexes, starting at the hub (index 1)
    packages = truck_packages.copy()  # Create a copy of the package list that can be modified
    package_data = create_package_hash()  # Get the package hash table
    packages_on_truck_data = []  # List to hold the complete data for each package on the truck

    # Get all data for each package on the truck and create a list containing the complete data for each package
    for package_id in packages:
        package_object = format(package_data.search(package_id)).split(',')
        packages_on_truck_data.append(package_object)

    # Iterate through the list of packages on the truck and build a list of stops optimized for distance.
    for i in truck_packages:
        previous_stop = get_address_from_id(optimized_route[truck_packages.index(i)])  # Identify the previous stop
        next_stop = find_next_stop(previous_stop, packages)  # Find the next closest stop from the remaining packages
        optimized_route.append(get_address_index(next_stop))  # Add the address id for the next stop to the running list

        # If a stop has been found for a package, remove the package from the copied list
        for j in packages_on_truck_data:
            if next_stop == packages_on_truck_data[packages_on_truck_data.index(j)][1]:
                package_delivered = int(packages_on_truck_data[packages_on_truck_data.index(j)][0])
                packages.remove(package_delivered)

    # Remove 'None' values from the new list. 'None' is a result of packages delivered to the same stop
    if None in list(optimized_route):
        optimized_route = list(filter(None, optimized_route))

    # Return to the hub, make it the last stop on the new list
    optimized_route.append(1)

    return optimized_route


# Gets the index from addresses.csv for a given address string
def get_address_index(address):
    address_data = get_address_data()
    address_index = None
    for row in address_data:
        if address == row[2]:
            address_index = int(row[0])
    return address_index


# Gets the address from addresses.csv for a given address index
def get_address_from_id(address_id):
    address_data = get_address_data()
    address = None
    for row in address_data[1:28]:  # skip the first row
        if address_id == int(row[0]):
            address = str(row[2])
    return address


# Gets the total distance from a list of address indexes
def get_total_distance(address_index_list):
    total_distance = 0.0

    # Iterate through the address index list and add the distance between each pair of addresses
    for i in address_index_list:
        if address_index_list[address_index_list.index(i) + 1]:
            address1 = get_address_from_id(i)
            address2 = get_address_from_id(address_index_list[address_index_list.index(i) + 1])
            total_distance += float(distance_between_addresses(address1, address2))
    return total_distance


# Calculate the delivery time for each package using the optimized route and departure time
def get_package_delivery_times(truck_route, departure_time):
    route = truck_route.copy()  # make a copy of the truck route so that it can be modified
    route.pop()  # remove the last item from the truck route to prevent duplicate keys in the next step

    # Initialize a dictionary of addresses IDs and the time at each stop.
    time_at_stop = dict.fromkeys(route, None)

    # Add a key for the last stop back at the hub.
    time_at_stop.update(back_to_hub=None)

    for address_id, time in time_at_stop.items():
        # Set the hub to the departure time
        if address_id == 1:
            time_at_stop.update({1: departure_time})

        # Calculate time of arrival back at the hub
        elif address_id == 'back_to_hub':
            address1 = get_address_from_id(route[-1])
            address2 = get_address_from_id(1)

            # Get the number of minutes between stops based on the distance and speed of the truck (18 mph)
            distance = float(distance_between_addresses(address1, address2))
            minutes_between_stops = math.ceil((distance / 18) * 60)

            # Add the number of minutes to the time at the previous stop
            previous_stop_time = datetime.strptime(time_at_stop.get(route[-1]), '%H:%M')
            next_stop_timestamp = previous_stop_time + timedelta(minutes=minutes_between_stops)
            next_stop_time = next_stop_timestamp.strftime('%H:%M')  # extract H:M format from timestamp

            # Update the dictionary with the return time
            time_at_stop.update({'back_to_hub': next_stop_time})

        # Calculate the time each package is delivered
        else:
            address1 = get_address_from_id(route[route.index(address_id) - 1])
            address2 = get_address_from_id(address_id)

            # Get the number of minutes between stops based on the distance and speed of the truck (18 mph)
            distance = float(distance_between_addresses(address1, address2))
            minutes_between_stops = math.ceil((distance / 18) * 60)

            # Add the number of minutes to the time at the previous stop
            previous_stop_time = datetime.strptime(time_at_stop.get(route[route.index(address_id) - 1]), '%H:%M')
            next_stop_timestamp = previous_stop_time + timedelta(minutes=minutes_between_stops)
            next_stop_time = next_stop_timestamp.strftime('%H:%M')  # extract H:M format from timestamp

            # Update the dictionary with the stop time
            time_at_stop.update({address_id: next_stop_time})

    return time_at_stop


# Update package statuses based on a time entered by the user
def update_package_statuses(package_hash_table, truck_packages, delivery_times_dict, requested_time):
    packages_on_truck_data = []  # Initiate a list to store data for packages on the truck
    requested_timestamp = datetime.strptime(requested_time, '%H:%M')  # Convert user-entered time to a datetime object

    # Get all data for each package on the truck and create a list containing the complete data for each package
    for item in truck_packages:
        package_object = format(package_hash_table.search(item)).split(',')
        packages_on_truck_data.append(package_object)

    # Iterate through the delivery times dict and update package statuses as needed
    for address_id, time in delivery_times_dict.items():
        timestamp = datetime.strptime(time, '%H:%M')  # Convert time in dict to a datetime object

        # If hub departure is before the requested time, update all packages on the truck to 'En route' status
        if address_id == 1 and timestamp <= requested_timestamp:

            for package in packages_on_truck_data:

                # Create a new package object with most of the same data, but update the package status
                package_obj = Package(package_id=int(package[0]),
                                      address=package[1],
                                      city=package[2],
                                      state=package[3],
                                      zipcode=package[4],
                                      deadline=package[5],
                                      weight=package[6],
                                      delivery_status='En route')

                # Insert the package into the package hash table
                package_hash_table.insert(int(package[0]), package_obj)

        # Find delivery stops that occur before or at the user-entered time
        if timestamp <= requested_timestamp:
            address = get_address_from_id(address_id)  # Get the address string from the address ID

            # Loop through the packages on the truck and find which packages should be updated to 'Delivered' status
            for package in packages_on_truck_data:
                if address == package[1]:
                    # print(format(package_data.search(int(package[0]))).split(','))

                    # Create a new package object with most of the same data, but update the package status
                    package_obj = Package(package_id=int(package[0]),
                                          address=package[1],
                                          city=package[2],
                                          state=package[3],
                                          zipcode=package[4],
                                          deadline=package[5],
                                          weight=package[6],
                                          delivery_status='Delivered at ' + time)

                    # Insert the package into the package hash table
                    package_hash_table.insert(int(package[0]), package_obj)

    return package_hash_table
