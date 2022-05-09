import unittest
from db import collection, add_carpool, add_passenger, remove_carpool, remove_passenger
from objects import Carpool, User

class TestDBMethods(unittest.TestCase):

    @classmethod
    def create_driver(cls):
        return User('12345', 'Emil Kovacev')

    def create_carpool(self):
        event_name = 'going to the mall'
        driver = self.create_driver()
        carpool = Carpool('1234', event_name, 3, driver)
        return add_carpool(carpool)

    def test_add_carpool(self):
        event_name = 'going to the mall'
        driver = self.create_driver()
        carpool = Carpool('1234', event_name, 3, driver)
        carpool_id = add_carpool(carpool)

        retval = collection.find_one({'carpool_id': carpool_id})
        retval.pop('_id')
        self.assertTrue(retval == carpool.serialize())

    def test_remove_carpool(self):
        carpool_id = self.create_carpool()
        remove_carpool(carpool_id)

        retval = collection.find_one({'_id': carpool_id})
        self.assertTrue(retval is None)

    def test_add_passenger(self):
        carpool_id = self.create_carpool()
        passenger = User('12345678', 'Adam Russell')
        add_passenger(carpool_id, passenger)

        retval = collection.find_one({'carpool_id': carpool_id})
        self.assertTrue(passenger.serialize() in retval['passengers'])

    def test_remove_passenger(self):
        carpool_id = self.create_carpool()
        passenger = User('12345678', 'Adam Russell')
        add_passenger(carpool_id, passenger)
        retval = collection.find_one({'carpool_id': carpool_id})
        self.assertTrue(passenger.serialize() in retval['passengers'])

        remove_passenger(carpool_id, passenger.user_id)

        retval = collection.find_one({'carpool_id': carpool_id})
        self.assertTrue(passenger.serialize() not in retval['passengers'])


if __name__ == '__main__':
    unittest.main()
