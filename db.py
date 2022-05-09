import pymongo
from objects import Carpool, User

client = pymongo.MongoClient("localhost", 27017, serverSelectionTimeoutMS=5000)
db = client.carpoolbot
collection = db.carpools


def add_carpool(carpool: Carpool):
    result = collection.insert_one(carpool.serialize())
    if not result.acknowledged:
        raise ValueError

    return carpool.id

def get_carpool(carpool_id: str):
    return collection.find_one({'carpool_id': carpool_id})

def remove_carpool(carpool_id: str):
    collection.delete_one({'carpool_id': carpool_id})

def add_passenger(carpool_id: str, passenger: User):
    carpool = collection.find_one({'carpool_id': carpool_id})

    passengers = carpool['passengers']
    capacity = carpool['capacity']
    passengers.append(passenger.serialize())
    capacity += 1

    collection.update_one({'carpool_id': carpool_id},
                          {'$set': {'passengers': passengers, "capacity": capacity}})

    return passenger.user_id

def find_passenger(uid, lst):
    for i in range(len(lst)):
        if lst[i]['user_id'] == uid:
            return i
    raise ValueError

def remove_passenger(carpool_id: str, passenger_id: str):
    carpool = collection.find_one({'carpool_id': carpool_id})

    passengers = carpool['passengers']
    i = find_passenger(passenger_id, passengers)
    passengers.pop(i)

    collection.update_one({'carpool_id': carpool_id},
                          {'$set': {'passengers': passengers}})

def is_carpool(carpool_id):
    retval = collection.find_one({'carpool_id': carpool_id})
    return retval is not None

def all_carpools():
    return list(collection.find())
