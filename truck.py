from datetime import datetime, timedelta

class Truck:
    def __init__(self, capacity, speed, mileage, location, packages, delivery_time, depart_time, truck_number, total_time_traveled):
        self.capacity = capacity
        self.speed = speed
        self.mileage = mileage
        self.location = location
        self.packages = packages
        self.delivery_time = datetime.strptime(delivery_time, '%I:%M %p') if delivery_time else None
        self.depart_time = datetime.strptime(depart_time, '%I:%M %p')
        self.truck_number = truck_number
        self.total_time_traveled = timedelta()

        # print(f"DEBUG: Depart Time for Truck is set to: {self.depart_time}")

    def __repr__(self):
            return (f"{self.capacity}, {self.speed}, {self.mileage}, {self.location}, "
                    f"{self.packages}, {self.delivery_time}, {self.depart_time}, {self.truck_number}, {self.total_time_traveled}")