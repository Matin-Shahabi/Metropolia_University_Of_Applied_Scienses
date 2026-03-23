import random

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

print("====== Single Car ====== ")
car1 = Car("ABC-123", 142)
print("====== Initial properties ======")
print(f"Registration number: {car1.registration_number}")
print(f"Maximum speed: {car1.max_speed} km/h")
print(f"Current speed: {car1.current_speed} km/h")
print(f"Travelled distance: {car1.travelled_distance} km")

car1.accelerate(30)
car1.accelerate(70)
car1.accelerate(50)
print("\n====== After accelerating steps ======")
print(f"Current speed: {car1.current_speed} km/h")

car1.accelerate(-200)
print("====== After emergency brake ======")
print(f"Current speed: {car1.current_speed} km/h")

print("\n====== Car Race Simulation ======")
cars = []

for i in range(1, 11):
    max_speed = random.randint(100, 200)
    reg_number = f"ABC-{i}"
    car = Car(reg_number, max_speed)
    cars.append(car)

race_finished = False
hour = 0
while not race_finished:
    hour += 1
    for car in cars:
        speed_change = random.randint(-10, 15)
        car.accelerate(speed_change)
        car.drive(1)
        if car.travelled_distance >= 10000:
            race_finished = True

print(f"\n ====== Race finished after {hour} hours! ======")
print(f"{'RegNum':<8} {'MaxSpeed':<8} {'CurrSpeed':<11} {'Distance':<10}")
print("-" * 40)
for car in cars:
    print(f"{car.registration_number:<10} {car.max_speed:<8} {car.current_speed:<10} {car.travelled_distance:<10.2f}")