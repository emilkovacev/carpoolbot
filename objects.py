from typing import List


class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    def __eq__(self, other):
        if self.user_id == other.user_id and \
           self.username != other.username:
            print('invalid duplicate user!')
            raise ValueError

        return self.user_id == other.user_id

    def serialize(self):
        return {
            'user_id': self.user_id,
            'username': self.username
        }

class Carpool:
    def __init__(self, id, event_name, capacity, driver: User):
        self.id = id
        self.event_name = event_name
        self.driver: User = driver
        self.capacity = capacity
        self.passengers: List[User] = []

    def __eq__(self, other):
        return self.id == other.id

    def add_passenger(self, passenger):
        if not self.at_capacity():
            self.passengers.append(passenger)
            self.capacity += 1
        else:
            raise ValueError

    def serialize(self):
        return {
            'carpool_id': self.id,
            'event_name': self.event_name,
            'driver': self.driver.serialize(),
            'passengers': [x.serialize for x in self.passengers],
            'capacity': self.capacity
        }

    def at_capacity(self):
        return len(self.passengers) >= self.capacity
