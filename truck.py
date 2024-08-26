class Truck:
    def __init__(self, capacity, speed, mileage, location, packages, delivery_time, depart_time):
        self.capacity = capacity
        self.speed = speed
        self.mileage = mileage
        self.location = location
        self.packages = packages
        self.delivery_time = depart_time
        self.depart_time = depart_time

    def __repr__(self):
            return (f"{self.capacity}, {self.speed}, {self.mileage}, {self.location}, "
                    f"{self.packages}, {self.delivery_time}, {self.depart_time}")