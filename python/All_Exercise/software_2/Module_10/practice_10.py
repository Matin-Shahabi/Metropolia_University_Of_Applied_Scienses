import random


class Elevator:
    def __init__(self, bottom_floor, top_floor):
        self.bottom_floor = bottom_floor
        self.top_floor = top_floor
        self.current_floor = bottom_floor

    def floor_up(self):
        if self.current_floor < self.top_floor:
            self.current_floor += 1
        print(f"Elevator is now at floor {self.current_floor}")

    def floor_down(self):
        if self.current_floor > self.bottom_floor:
            self.current_floor -= 1
        print(f"Elevator is now at floor {self.current_floor}")

    def go_to_floor(self, target_floor):
        print(f"Moving to floor {target_floor} from floor {self.current_floor}")
        while self.current_floor < target_floor:
            self.floor_up()
        while self.current_floor > target_floor:
            self.floor_down()


print("====== Elevator Test ======")
elevator1 = Elevator(0, 10)
elevator1.go_to_floor(5)
elevator1.go_to_floor(0)


class Building:
    def __init__(self, bottom_floor, top_floor, num_elevators):
        self.bottom_floor = bottom_floor
        self.top_floor = top_floor
        self.elevators = [Elevator(bottom_floor, top_floor) for _ in range(num_elevators)]

    def run_elevator(self, elevator_number, target_floor):
        if 0 <= elevator_number < len(self.elevators):
            self.elevators[elevator_number].go_to_floor(target_floor)
        else:
            print("Invalid elevator number!")

    def fire_alarm(self):
        print("Fire alarm activated! Moving all elevators to bottom floor.")
        for elevator in self.elevators:
            elevator.go_to_floor(self.bottom_floor)


print("\n====== Building Test ======")
building = Building(0, 10, 3)
building.run_elevator(0, 7)
building.fire_alarm()


class Car:
    def __init__(self, registration_number, max_speed):
        self.registration_number = registration_number
        self.max_speed = max_speed
        self.current_speed = 0
        self.travelled_distance = 0

    def accelerate(self, speed_change):
        self.current_speed += speed_change
        if self.current_speed > self.max_speed:
            self.current_speed = self.max_speed
        elif self.current_speed < 0:
            self.current_speed = 0

    def drive(self, hours):
        self.travelled_distance += self.current_speed * hours


class Race:
    def __init__(self, name, distance_km, cars):
        self.name = name
        self.distance = distance_km
        self.cars = cars

    def hour_passes(self):
        for car in self.cars:
            speed_change = random.randint(-10, 15)
            car.accelerate(speed_change)
            car.drive(1)

    def print_status(self):
        print(f"\n====== Status of {self.name} ======")
        print(f"{'RegNumber':<10} {'MaxSpeed':<8} {'CurrSpeed':<10} {'Distance':<10}")
        print("-" * 45)
        for car in self.cars:
            print(
                f"{car.registration_number:<10} {car.max_speed:<8} {car.current_speed:<10} {car.travelled_distance:<10.2f}")

    def race_finished(self):
        for car in self.cars:
            if car.travelled_distance >= self.distance:
                return True
        return False


print("\n====== Grand Demolition Derby ======")

cars = []
for i in range(1, 11):
    max_speed = random.randint(100, 200)
    reg_number = f"CAR-{i}"
    cars.append(Car(reg_number, max_speed))

race = Race("Grand Demolition Derby", 8000, cars)

hours_passed = 0
while not race.race_finished():
    hours_passed += 1
    race.hour_passes()
    if hours_passed % 10 == 0:
        race.print_status()

race.print_status()
print(f"\n====== Race finished after {hours_passed} hours! ======")