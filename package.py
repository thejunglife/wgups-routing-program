
class Package:
    def __init__(self, package_id, delivery_address, delivery_deadline, delivery_city, delivery_state, delivery_zip, package_weight, delivery_status, delivery_time, depart_time, truck_number):
        self.package_id = package_id
        self.delivery_address = delivery_address
        self.delivery_city = delivery_city
        self.delivery_state = delivery_state
        self.delivery_zip = delivery_zip
        self.delivery_deadline = delivery_deadline
        self.package_weight = package_weight
        self.delivery_status = 'At Hub' # Default
        self.delivery_time = delivery_time
        self.depart_time = None
        self.truck_number = None
    def __repr__(self):
        return(f"{self.package_id}, {self.delivery_address}, {self.delivery_city}, {self.delivery_state}, "
               f"{self.delivery_zip}, {self.delivery_deadline}, {self.package_weight}, {self.delivery_status}, {self.delivery_time if self.delivery_time else 'Not Delivered Yet'}, {self.truck_number}")

    def update_status(self, status, delivery_time=None, depart_time=None):
        self.delivery_status = status
        if delivery_time:
            self.delivery_time = delivery_time
        if depart_time:
            self.depart_time = depart_time