
class Package:
    def __init__(self, package_id, delivery_address, delivery_deadline, delivery_city, delivery_state, delivery_zip, package_weight, delivery_status):
        self.package_id = package_id
        self.delivery_address = delivery_address
        self.delivery_city = delivery_city
        self.delivery_state = delivery_state
        self.delivery_zip = delivery_zip
        self.delivery_deadline = delivery_deadline
        self.package_weight = package_weight
        self.delivery_status = delivery_status

    def __repr__(self):
        return(f"{self.package_id}, {self.delivery_address}, {self.delivery_city}, {self.delivery_state} "
               f"{self.delivery_zip}, {self.delivery_deadline} {self.package_weight}, {self.delivery_status}")