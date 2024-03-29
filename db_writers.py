import pymongo
import time
import sys
import json

class GoogleCloudStorageWriter():
    def __init__(self, host = "127.0.0.1", port = 27017):
        timeout = 5000
        self.client = pymongo.MongoClient(host=host, port=port, serverSelectionTimeoutMS=timeout)
        try:
            result = self.client.admin.command("ismaster")
            print("Mongo connection esteblished : " + str(self.client))
        except pymongo.errors.ServerSelectionTimeoutError as e:
            print("Server did not managed to set connection in " + (str(timeout/1000)) + " second. Likely that server is unavailable")
            raise ValueError("Can't establish connection. Wrong host or/and port : " + host + ":" + str(port))


class MongoWriter():
    def __init__(self, host = "127.0.0.1", port = 27017):
        timeout = 5000
        self.client = pymongo.MongoClient(host=host, port=port, serverSelectionTimeoutMS=timeout)
        try:
            result = self.client.admin.command("ismaster")
            print("Mongo connection esteblished : " + str(self.client))
        except pymongo.errors.ServerSelectionTimeoutError as e:
            print("Server did not managed to set connection in " + (str(timeout/1000)) + " second. Likely that server is unavailable")
            raise ValueError("Can't establish connection. Wrong host or/and port : " + host + ":" + str(port))

    def writePowerUsersToCollection(self, powerUsers, database, collection):
        db = self.client[database]
        collection = db[collection]
        
        print("powerUsers size : " + str(sys.getsizeof(powerUsers.reset_index().to_json(orient="records"))/1024/1024/1024))

        print("Creating json data. It might take a while")
        tm0 = time.time()
        json_data = json.loads(powerUsers.reset_index().to_json(orient="records"))
        tm1 = time.time()
        print("json_data : " + str(sys.getsizeof(json_data)/1024/1024/1024))
        print("Creating json data took " +str(tm1-tm0))

        try:
            collection.drop()
            tm0 = time.time()
            collection.insert_many(json_data)
            tm1 = time.time()
        except Exception as e:
            print(e)

        print("powerUsers is written to the MongoDB : " + str(self.client.address) + "." + str(db.name) + "." + str(collection.name))
        print("Mongo insert took " + str(tm1 - tm0) + " seconds")