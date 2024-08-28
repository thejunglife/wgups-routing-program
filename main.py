# Paul Jung ID 010186698

import csv
from datetime import datetime, timedelta
import datetime
from package import Package
from truck import Truck
from hash_table import HashTable


# Creates a Package from csv package file into hash_table
def load_packages(file_path):
    # Initialize a hash table and load the package data from CSV file
    # Each package information will be stored in package object
    # Will use the id as the key in the hash table for quick retrieval
    hash_table = HashTable()

    # Open the CSV file containing package data
    with open(file_path, mode='r') as package_file:
        package_data = csv.reader(package_file)

        # Iterate through each row in the CSV file
        for data in package_data:
            package_id = int(data[0])
            delivery_address = data[1]
            delivery_city = data[2]
            delivery_state = data[3]
            delivery_zip = data[4]
            delivery_deadline = data[5]
            delivery_weight = data[6]

            # These will not be updated from CSV but dynamically during the delivery process
            delivery_status = ''
            delivery_time = ''
            depart_time = ''
            truck_number = ''

            # Create a Package object with the data
            package = Package(
                package_id,
                delivery_address,
                delivery_city,
                delivery_state,
                delivery_zip,
                delivery_deadline,
                delivery_weight,
                delivery_status,
                delivery_time,
                depart_time,
                truck_number
            )
            # insert package data into hash table
            hash_table.insert(package_id, package)

    return hash_table


# load addresses in to dict
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
truck1 = Truck(16, 18, 0, "Hub", [], None, "09:05 AM", 1, total_time_traveled=None)
truck2 = Truck(16, 18, 0, "Hub", [], None, "08:00 AM", 2, total_time_traveled=None)
truck3 = Truck(16, 18, 0, "Hub", [], None, "10:20 AM", 3, total_time_traveled=None)

truck1.packages = [6, 25, 28, 32, 31, 2, 4, 5, 7, 34, 39, 35, 33]  # 13 will wait for 9:05 AM packages
truck2.packages = [18, 36, 3, 38, 20, 21, 13, 15, 19, 16, 14, 37, 40, 1, 29, 30]  # 16
truck3.packages = [8, 9, 10, 11, 12, 17, 22, 23, 24, 26, 27]  # 11

# Use nearest neighbor algorithm to deliver packages with the trucks
def deliver_packages(truck):
    # Start at the hub location 0 (4001 South 700 East)
    current_location = 0
    total_distance = 0
    delivery_time = truck.depart_time

    # Update status of packages to En Route once it departs from hub
    for package_id in truck.packages:
        package = hash_table.lookup(package_id)
        package.truck_number = truck.truck_number
        package.update_status("En route", depart_time=truck.depart_time)

    # separate packages that need to be delivered by 10:30 AM (urgent) and EOD (regular)
    urgent_packages = []
    regular_packages = []

    # Iterate trough packages to classify based on delivery deadline
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

        # Find the nearest package to the current location
        for package in urgent_packages:
            package_address_id = list(addresses.keys())[list(addresses.values()).index(package.delivery_address)]
            distance = get_distance(distances, current_location, package_address_id)

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_package = package

        # Deliver the nearest urgent package then remove from list
        urgent_packages.remove(nearest_package)
        truck.packages.remove(nearest_package.package_id)

        # Calculate total distance and time traveled
        total_distance += nearest_distance
        time_to_next_stop = timedelta(hours=nearest_distance / truck.speed)
        delivery_time = delivery_time + datetime.timedelta(hours=nearest_distance / truck.speed)
        truck.total_time_traveled += time_to_next_stop

        # total mileage
        truck.mileage = total_distance

        # Update the package's status to "Delivered"
        nearest_package.update_status("Delivered", delivery_time.strftime('%I:%M %p'))

        # Move truck's current location to the package's address
        current_location = list(addresses.keys())[list(addresses.values()).index(nearest_package.delivery_address)]

    # Deliver remaining packages
    while regular_packages:
        nearest_package = None
        nearest_distance = float('inf')

        # Find the nearest package to the current location
        for package in regular_packages:
            package_address_id = list(addresses.keys())[list(addresses.values()).index(package.delivery_address)]
            distance = get_distance(distances, current_location, package_address_id)

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_package = package
        # Deliver the nearest regular package then remove from list
        regular_packages.remove(nearest_package)
        truck.packages.remove(nearest_package.package_id)

        # Calculate total distance and time traveled
        total_distance += nearest_distance
        time_to_next_stop = timedelta(hours=nearest_distance / truck.speed)
        delivery_time = delivery_time + datetime.timedelta(hours=nearest_distance / truck.speed)
        truck.total_time_traveled += time_to_next_stop #time traveled

        #total mileage
        truck.mileage = total_distance

        # Update the package's status
        nearest_package.update_status("Delivered", delivery_time.strftime('%I:%M %p'))

        # Move truck's current location to the package's address
        current_location = list(addresses.keys())[list(addresses.values()).index(nearest_package.delivery_address)]

    # After delivering all packages return back to hub location 0 (#4001 South 700 East HUB)
    if current_location != 0:
        distance_to_hub = get_distance(distances, current_location, 0)
        total_distance += distance_to_hub
        truck.mileage = total_distance

    return total_distance

# Helper method for CLI to prevent repetition to look up packages
def check_package_status(package_id, time_to_check):
        package = hash_table.lookup(package_id)
        if package:
            # Checks for package 9 to switch address at 10:20 AM
            if package_id == 9 and time_to_check >= datetime.datetime.strptime("10:20 AM", "%I:%M %p"):
                package.delivery_address = "410 S State St"
                package.delivery_city = "Salt Lake City"
                package.delivery_state = "UT"
                package.delivery_zip = "84111"
                hash_table.insert(9, package)

            depart_time = package.depart_time

            # Assign depart time to update status
            if package_id in truck1.packages:
                depart_time = truck1.depart_time
                package.truck_number = truck1.truck_number
            elif package_id in truck2.packages:
                depart_time = truck2.depart_time
                package.truck_number = truck2.truck_number
            elif package_id in truck3.packages:
                depart_time = truck3.depart_time
                package.truck_number = truck3.truck_number

            if package.delivery_time:
                delivery_time = datetime.datetime.strptime(package.delivery_time, '%I:%M %p')
            else:
                delivery_time = None

            # Tells status of package depending on input time
            if time_to_check < depart_time:
                status = f"At the Hub waiting to go to {package.delivery_address} by Truck {package.truck_number}"
            elif delivery_time and time_to_check >= delivery_time:
                status = f"Delivered at {package.delivery_time} (Delivery deadline: {package.delivery_deadline}) to {package.delivery_address} by Truck {package.truck_number}"
            else:
                status = f"En route to {package.delivery_address} by Truck {package.truck_number}"

            print(f"Package {package.package_id} status at {time_to_check.strftime('%I:%M %p')}: {status}")
        else:
            print(f"No package found with ID {package_id}")

# load the trucks to deliver
deliver_packages(truck1)
deliver_packages(truck2)
deliver_packages(truck3)

class Main:

    # Main CLI
    while True:
        # Main Menu
        print("\nMenu:")
        print("1. Check Package Status")
        print("2. View Total Mileage/Time Traveled")
        print("3. Exit")

        try:
            choice = int(input("Please choose an option (1-3): "))

            if choice == 1:
                # Sub Menu for Packages
                print("\nPackage Status:")
                print("1. Search Single Package")
                print("2. View All Packages")
                package_choice = int(input("Please choose an option (1-2): "))

                time_input = input("Enter the time (e.g., 08:30 AM) to check the package status: ")
                time_to_check = datetime.datetime.strptime(time_input, '%I:%M %p')
                # For single package status
                if package_choice == 1:
                    package_id = int(input("Enter the package ID (1-40) to view details: "))
                    check_package_status(package_id, time_to_check)
                # All package status
                elif package_choice == 2:
                    print(f"Status of all packages at {time_input}:")
                    for package_id in range(1, 41):
                        check_package_status(package_id, time_to_check)

            elif choice == 2:
                # Option 2: View Truck miles/time traveled
                print(f"Truck 1 total distance traveled: {truck1.mileage} miles")
                print(f"Truck 2 total distance traveled: {truck2.mileage} miles")
                print(f"Truck 3 total distance traveled: {truck3.mileage} miles")
                print(f"Total miles of all three trucks traveled: {truck1.mileage + truck2.mileage + truck3.mileage} miles")
                print(f"Truck 1 total time traveled: {str(truck1.total_time_traveled)}")
                print(f"Truck 2 total time traveled: {str(truck2.total_time_traveled)}")
                print(f"Truck 3 total time traveled: {str(truck3.total_time_traveled)}")
                print(f"Total time traveled of all three trucks: {truck1.total_time_traveled + truck2.total_time_traveled + truck3.total_time_traveled}")


            elif choice == 3:
                # Option 3: Exit
                print("Exiting the program. Goodbye!")
                break

            else:
                print("Invalid choice. Please select an option from the menu.")

        except ValueError:
            print("Invalid input")
