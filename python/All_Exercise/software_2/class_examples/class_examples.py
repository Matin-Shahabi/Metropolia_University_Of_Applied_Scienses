# class Character:
#     def __init__(self, name):
#         self.name = name
#
#     def introduce(self):
#         print(self.name)
#
#
# class MarioCharacter(Character):
#     def __init__(self, name, lives):
#         super().__init__(name)
#         self.lives = lives
#
#     def jump(self):
#         print(f"{self.name} jumps up")
#
#
# class FireMario(MarioCharacter):
#
#     def throw_fireball(self):
#         print(f"{self.name} throws a fireball")
#
#
# class SuperMario(MarioCharacter):
#
#
#     def yell(self):
#         print(f"{self.name} yells Mama mia !")
#
#
# class SuperFireMario(FireMario, SuperMario):
#     pass
#
#
# mario_1 = MarioCharacter(name="Mario 1", lives=1)
# firemario_1 = FireMario(name="FireMario 1", lives=1)
#
# mario_1.introduce()
# firemario_1.introduce()
# firemario_1.jump()
# firemario_1.throw_fireball()
#
# superMrio1 = SuperMario(name="Super Mario 1", lives=1)
# superfiremario = SuperFireMario(name="Super Fire Mario 1", lives=1)
# superfiremario.introduce()
# superfiremario.jump()
# superfiremario.throw_fireball()
# superfiremario.yell()






# Requests & json






import requests,json



keyword = input("Please enter your keyword: ")
request = "https://api.tvmaze.com/search/shows?q=" + keyword

try:
    response = requests.get(request)
    if response.status_code == 200:
        json_response = response.json()
        for r in json_response:
            print(r["show"]["name"])
except requests.exceptions.RequestException as e:
    print("0-0, Sorry :( , The request could not be completed at this time.")
    print(e)




response = requests.get(request).json()
# json converts in dictionary type

# response = response.get(request)
# print(response.status_code)

#  show status code

print(json.dumps(response, indent=2))
#  the indent make pretty-print of web

print(len(response))
# the length of response or dictionaries

for r in response:
    print(r["show"]["name"])
# print(response)