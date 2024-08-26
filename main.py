# Paul Jung ID 010186698

import csv
import datetime
from package import Package
from truck import Truck
from hash_table import HashTable



# Creates a Package from csv package file into hash_table
def load_packages(file_path):
    hash_table = HashTable()
    with open(file_path, mode='r') as package_file:
        package_data = csv.reader(package_file)
        for data in package_data:
            package_id = int(data[0])
            delivery_address = data[1]
            delivery_city = data[2]
            delivery_state = data[3]
            delivery_zip = data[4]
            delivery_deadline = data[5]
            delivery_weight = data[6]
            delivery_status = data[7]

            # Create a Package object
            package = Package(
                package_id,
                delivery_address,
                delivery_city,
                delivery_state,
                delivery_zip,
                delivery_deadline,
                delivery_weight,
                delivery_status
            )
            #insert package data into hash table
            hash_table.insert(package_id, package)

    return hash_table

#load addresses in to dict
def load_addresses(file_path):
    addresses = {}
    with open(file_path, mode='r') as address_file:
        address_data = csv.reader(address_file)
        for data in address_data:
            address_id = int(data[0])
            address_name = data[1]
            address_number = data[2]
            addresses[address_id] = f"{address_number}"
    return addresses

# load distance table file in 2d list
def load_distances(file_path):
    distances = []
    with open(file_path, mode='r') as distance_file:
        distance_data = csv.reader(distance_file)
        for data in distance_data:
            distances.append(list(map(float, data)))
    return distances

# load all csv files
hash_table = load_packages('csv/package_file.csv')
addresses = load_addresses('csv/address_file.csv')
distances = load_distances('csv/distance_table_file.csv')

# get distance (miles) between two addresses
def get_distance(distances, from_address, to_address):
    row, col = max(from_address, to_address), min(from_address, to_address)
    return distances[row][col]

# get address by id
def get_address(address_dict, address_id):
    return address_dict.get(address_id, None)

# Create three truck objects
truck1 = Truck(16, 18, 0, "Hub", [], "09:05 AM", "09:05 AM" )
truck2 = Truck(16, 18, 0, "Hub", [], "08:00 AM", "08:00 AM" )
truck3 = Truck(16, 18, 0, "Hub", [], "10:20 AM", "10:20 AM" )

truck1.packages = [6, 25, 28, 32, 31, 2, 4, 5, 7, 34, 39, 35, 33]#13 green will wait for 9:05 AM packages
truck2.packages = [18, 36, 3, 38, 20, 21, 13, 15, 19, 16, 14, 37, 40, 1, 29, 30] # 16 yellow
truck3.packages = [8, 9, 10, 11, 12, 17, 22, 23, 24, 26, 27] #11

# Use nearest neighbor algorithm to deliver packages with the trucks
def deliver_packages(truck, distances, addresses, hash_table):
    # Check if it's 10:20 AM or later and if package #9 is in this truck's load
    current_time = datetime.datetime.strptime("10:15 AM", "%I:%M %p") # temp time
    if 9 in truck.packages and current_time >= datetime.datetime.strptime("10:20 AM", "%I:%M %p"):
            package_9 = hash_table.lookup(9)
            package_9.delivery_address = "410 S State St"
            package_9.delivery_city = "Salt Lake City"
            package_9.delivery_state = "UT"
            package_9.delivery_zip = "84111"
            hash_table.insert(9, package_9)  # Update the package in the hash table
            print(f"Address for package 9 updated to {package_9.delivery_address}, {package_9.delivery_city}, {package_9.delivery_state} {package_9.delivery_zip} at {truck.depart_time}")

    current_location = 0
    total_distance = 0
    delivery_time = datetime.datetime.strptime(truck.depart_time,'%I:%M %p')
    delivery_log = []

    # Update packages to enroute once it departs hub
    for package_id in truck.packages:
        package = hash_table.lookup(package_id)
        package.update_status("Enroute")

    # seperate packages that need to be delivered by 10:30 AM
    urgent_packages = []
    regular_packages = []

    for package_id in truck.packages:
        package = hash_table.lookup(package_id)
        if package.delivery_deadline == '10:30 AM':
            urgent_packages.append(package)
        else:
            regular_packages.append(package)


    # Deliver all urgent packages first Deadline: 10:30 AM
    while urgent_packages:
        nearest_package = None
        nearest_distance = float('inf')

        for package in urgent_packages:
            package_address_id = list(addresses.keys())[list(addresses.values()).index(package.delivery_address)]
            distance = get_distance(distances, current_location, package_address_id)

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_package = package

            # Deliver the nearest urgent package
        urgent_packages.remove(nearest_package)
        truck.packages.remove(nearest_package.package_id)
        total_distance += nearest_distance
        delivery_time += datetime.timedelta(hours=nearest_distance / truck.speed)

        # Update the package's status to "Delivered"
        nearest_package.update_status(f"Delivered")
        delivery_log.append(f"Package {nearest_package.package_id} delivered to {nearest_package.delivery_address} at {delivery_time.strftime('%I:%M %p')}")

        # Move truck's current location to the package's address
        current_location = list(addresses.keys())[list(addresses.values()).index(nearest_package.delivery_address)]

    # Deliver remaining packages
    while regular_packages:
        nearest_package = None
        nearest_distance = float('inf')

        for package in regular_packages:
            # package = hash_table.lookup(package_id)
            print(f"Looking for: {package.delivery_address}")
            print(f"Available addresses: {list(addresses.values())}")
            package_address_id = list(addresses.keys())[list(addresses.values()).index(package.delivery_address)]
            distance = get_distance(distances, current_location, package_address_id)

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_package = package


        regular_packages.remove(nearest_package)
        truck.packages.remove(nearest_package.package_id)
        total_distance += nearest_distance
        delivery_time += datetime.timedelta(hours=nearest_distance / truck.speed)

        # Update the package's status
        nearest_package.update_status(f"Delivered")
        delivery_log.append(f"Package {nearest_package.package_id} delivered to {nearest_package.delivery_address} at {delivery_time.strftime('%I:%M %p')}")

        # Move truck's current location to the package's address
        current_location = list(addresses.keys())[list(addresses.values()).index(nearest_package.delivery_address)]

    return total_distance, delivery_log



def main():
    total_mileage = 0

    # Deliver packages for Truck 1 and capture the log
    mileage1, log1 = deliver_packages(truck1, distances, addresses, hash_table)
    total_mileage += mileage1

    # Deliver packages for Truck 2 and capture the log
    mileage2, log2 = deliver_packages(truck2, distances, addresses, hash_table)
    total_mileage += mileage2

    # Deliver packages for Truck 3 and capture the log
    mileage3, log3 = deliver_packages(truck3, distances, addresses, hash_table)
    total_mileage += mileage3

    # Print logs for each truck
    print("Truck 1 Delivery Log:")
    for entry in log1:
        print(entry)
    print(f"Total mileage for Truck 1: {mileage1:.2f} miles\n")

    print("Truck 2 Delivery Log:")
    for entry in log2:
        print(entry)
    print(f"Total mileage for Truck 2: {mileage2:.2f} miles\n")

    print("Truck 3 Delivery Log:")
    for entry in log3:
        print(entry)
    print(f"Total mileage for Truck 3: {mileage3:.2f} miles\n")

    print(f"Total mileage traveled by all trucks: {total_mileage:.2f} miles")

    # Optionally, you can output the final delivery status of each package
    for package_id in range(1, 41):
        package = hash_table.lookup(package_id)
        print(f"Package {package_id}: {package.delivery_status}")

if __name__ == "__main__":
    main()

# def main():
#     total_mileage = 0
#
#     total_mileage += deliver_packages(truck1, distances, addresses, hash_table)
#     total_mileage += deliver_packages(truck2, distances, addresses, hash_table)
#     total_mileage += deliver_packages(truck3, distances, addresses, hash_table)
#
#     print(f"Total mileage traveled by all trucks: {total_mileage:.2f} miles")
#
#     # Optionally, you can output the final delivery status of each package
#     for package_id in range(1, 41):
#         package = hash_table.lookup(package_id)
#         print(f"Package {package_id}: {package.delivery_status}")
#
# if __name__ == "__main__":
#     main()
# class Main:
#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.package_hash_table = None
#
#     def load_data(self):
#         self.package_hash_table = load_packages(self.file_path)
#
#     def display_data(self):
#         print(self.package_hash_table)
#
#     def lookup_package(self, package_id):
#         package = self.package_hash_table.lookup(package_id)
#         if package:
#             print(f"Package {package_id} found: {package}")
#         else:
#             print(f"Package {package_id} not found")
#
#     def run(self):
#         self.load_data()
#         self.display_data()
#
#         package_id = 40
#         self.lookup_package(package_id)
#
# if __name__ == "__main__":
#     app = Main('csv/package_file.csv')
#     app.run()