# Example_1

class Publication:
    def __init__(self,name):
        self.name = name


class Book(Publication):
    def __init__(self,name,author,page_count):
        super().__init__(name)
        self.author = author
        self.page_count = page_count

    def print_information(self):
        print(f"book name : {self.name} , author : {self.author} , page_count : {self.page_count}\n")


class Magazine(Publication):
    def __init__(self,name,chief_editor):
        super().__init__(name)
        self.chief_editor = chief_editor

    def print_information(self):
        print(f"Magazine name : {self.name} , chief editor : {self.chief_editor}")




book_1 = Book("Compartment No.6","Rosa Liksom",192)
magazine_1 = Magazine("Donald Duck","Aki Hyypa")
magazine_1.print_information()
book_1.print_information()






# Example_2

class Car:
    def __init__(self,registration_number,max_speed):
        self.registration_number = registration_number
        self.max_speed = max_speed
        self.current_speed = 0
        self.odometer = 0

    def accelerate(self,speed):
        self.current_speed = speed
        if self.current_speed > self.max_speed:
            self.current_speed = self.max_speed
        if self.current_speed < 0:
            self.current_speed = 0

    def drive(self,hours):
        self.odometer += self.current_speed * hours

class ElectricCar(Car):
    def __init__(self,registration_number,max_speed,battery_capacity):
        super().__init__(registration_number,max_speed)
        self.battery_capacity = battery_capacity

class GasolineCar(Car):
    def __init__(self,registration_number,max_speed,tank_volume):
        super().__init__(registration_number,max_speed)
        self.tank_volume = tank_volume


electric_car_1 = ElectricCar("ABC-15",180,52.5)
gasoline_car_1 = GasolineCar("ACD-123",165,32.3)

electric_car_1.accelerate(100)
gasoline_car_1.drive(120)
electric_car_1.drive(3)
gasoline_car_1.drive(3)
print(f"Electric car : {electric_car_1.registration_number} distance : {electric_car_1.odometer}")
print(f"Gasoline car : {gasoline_car_1.registration_number} distance : {gasoline_car_1.odometer}")