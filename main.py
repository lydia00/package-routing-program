from package import create_package_hash, get_package_info
from distance import find_optimized_route, get_package_delivery_times, update_package_statuses, get_total_distance

'''
WGUPS Package Routing Program
Lydia Husser
ID: 001427998
'''

# Create the package hash table
package_data = create_package_hash()

# Address for the package hub
hub = '4001 South 700 East'

# Packages on each truck, identified by package ID
truck1_packages = [1, 8, 13, 14, 15, 16, 19, 20, 21, 29, 30, 31, 34, 37, 40]
truck2_packages = [2, 3, 6, 7, 11, 17, 18, 25, 26, 27, 28, 33, 35, 36, 38, 39]
truck3_packages = [4, 5, 9, 10, 12, 22, 23, 24, 32]

# Generate the route for each truck. A route is an optimized list of addresses, identified by address ID
truck1_route = find_optimized_route(truck1_packages)
truck2_route = find_optimized_route(truck2_packages)
truck3_route = find_optimized_route(truck3_packages)

# Departure time for each truck
truck1_departure = '08:00'
truck2_departure = '09:15'
truck3_departure = '10:30'

# Delivery times for each package based on the optimized route and truck departure time
truck1_delivery_times = get_package_delivery_times(truck1_route, truck1_departure)
truck2_delivery_times = get_package_delivery_times(truck2_route, truck2_departure)
truck3_delivery_times = get_package_delivery_times(truck3_route, truck3_departure)

print('\nHello, welcome to the WGUPS delivery routing program.')
print('-----------------------------------------------------')


# Interface to view package statuses, package data, and truck distances.
def interface():
    user_selection = input('\nType a number and press Enter to select an option:\n'
                           '1 - View status of all packages at a specified time\n'
                           '2 - View data for a package\n'
                           '3 - View total distance traveled by all trucks\n'
                           '0 - Exit the program\n')

    # Take the user entered time, update package delivery statuses, and print the complete list of packages
    if user_selection == '1':
        user_time = input('Enter a time in HH:MM format (using the 24-hour clock) and press Enter.\n')
        print('\nPackage statuses at', user_time)
        print('-------------------------')

        update_package_statuses(package_data, truck1_packages, truck1_delivery_times, user_time)
        update_package_statuses(package_data, truck2_packages, truck2_delivery_times, user_time)
        update_package_statuses(package_data, truck3_packages, truck3_delivery_times, user_time)
        print('ID | Address | City | State | Zip | Due | Wt. | Status')
        for i in range(len(package_data.table)):
            package_statuses = format(package_data.search(i + 1)).split(',')
            print(package_statuses[0], '|', package_statuses[1], '|', package_statuses[2], '| ', package_statuses[3],
                  ' |', package_statuses[4], '|', package_statuses[5], '|', package_statuses[6],
                  '|', package_statuses[7])

        input('\nPress Enter to continue.')
        interface()

    # Print information for a specific package
    elif user_selection == '2':
        package_id = input('Enter a package ID and press Enter.\n')
        package_info = get_package_info(package_data, int(package_id))
        print('Data for package no.', package_id + ':')
        print('ID:', package_info[0],
              '\nAddress:', package_info[1],
              '\nCity:', package_info[2],
              '\nState:', package_info[3],
              '\nZip:', package_info[4],
              '\nDeadline:', package_info[5],
              '\nWeight:', package_info[6])

        input('\nPress Enter to continue.')
        interface()

    # Print the distance traveled by each truck and the total distance.
    elif user_selection == '3':
        truck1_distance = round(get_total_distance(truck1_route), 2)
        truck2_distance = round(get_total_distance(truck2_route), 2)
        truck3_distance = round(get_total_distance(truck3_route), 2)

        print('Truck 1 distance:', truck1_distance)
        print('Truck 2 distance:', truck2_distance)
        print('Truck 3 distance:', truck3_distance)
        print('Total distance:', truck1_distance + truck2_distance + truck3_distance)

        input('\nPress Enter to continue.')
        interface()

    # Stop the program
    elif user_selection == '0':
        print('You have exited the program.')
        SystemExit

    # Prompt user for a different selection
    else:
        print('Invalid selection, please try again.\n')
        interface()


# Run the user interface
interface()
