import csv

from hashtable import ChainingHashTable


# Class that defines a package
class Package:
    # Constructor for the package class.
    def __init__(self, package_id, address, city, state, zipcode, deadline, weight, delivery_status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.delivery_status = delivery_status

    # Customize string output to avoid returning the object reference
    def __str__(self):
        return '%s,%s,%s,%s,%s,%s,%s,%s' % (self.package_id, self.address, self.city, self.state, self.zipcode,
                                            self.deadline, self.weight, self.delivery_status)


'''
Package operations
'''


# Function to read package data from a CSV file and return it in a hash table
def create_package_hash():
    # Create a hash table object
    package_hash = ChainingHashTable(40)

    # Read CSV file
    with open('data/packages.csv') as packages:
        package_data = csv.reader(packages, delimiter=',')
        next(package_data)  # skip the header row
        for item in package_data:
            package_id = int(item[0])
            address = item[1]
            city = item[2]
            state = item[3]
            zipcode = item[4]
            deadline = item[5]
            weight = item[6]
            delivery_status = 'At the hub'

            # Create a package object
            package = Package(package_id, address, city, state, zipcode, deadline, weight, delivery_status)

            # Add package to hash table
            package_hash.insert(package_id, package)

    return package_hash


# Get the data for a specific package at any time
def get_package_info(package_hash_table, package_id):
    package_object = format(package_hash_table.search(package_id)).split(',')
    package_object.pop()
    return package_object
