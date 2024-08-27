
class HashTable:
    def __init__(self, packages=40):
        self.packages = packages
        self.table = []
        for i in range(packages):
            self.table.append([])

    def _hash(self, package_id):
        return package_id % self.packages

    # Inserts new package entry into the hash table
    def insert(self, package_id, package_data):
        # Calculate the index using the hash function
        package_slot = self._hash(package_id)
        package_list = self.table[package_slot]

        # Update package_id if already in package_slot
        for entry in package_list:
            if entry[0] == package_id:
                entry[1] = package_data
                return True

        # Insert item to the end of package_list if not in package_slot
        package_entry = [package_id, package_data]
        package_list.append(package_entry)
        return True

    # Lookup items in hash table
    def lookup(self, package_id):
        package_slot = self._hash(package_id)
        package_list = self.table[package_slot]

        for entry in package_list:
            if package_id == entry[0]:
                return entry[1]
            return None # only if package is not found


    # Using f string
    def __repr__(self):
        # Create a string representation of the hash table
        return '\n'.join(f"Bucket {i}: {bucket}" for i, bucket in enumerate(self.table) if bucket)

