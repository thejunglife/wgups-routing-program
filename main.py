# Paul Jung ID 010186698

import csv
from package import Package
from hash_table import HashTable


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

            hash_table.insert(package_id, package)

    return hash_table

class Main:
    def __init__(self, file_path):
        self.file_path = file_path
        self.package_hash_table = None

    def load_data(self):
        self.package_hash_table = load_packages(self.file_path)

    def display_data(self):
        print(self.package_hash_table)

    def lookup_package(self, package_id):
        package = self.package_hash_table.lookup(package_id)
        if package:
            print(f"Package {package_id} found: {package}")
        else:
            print(f"Package {package_id} not found")

    def run(self):
        self.load_data()
        self.display_data()

        package_id = 40
        self.lookup_package(package_id)

if __name__ == "__main__":
    app = Main('csv/WGUPS Package File.csv')
    app.run()