import datetime
import os
import sys
from dotenv import load_dotenv
from power_user_optimism import events_data_connectors as dc
from power_user_optimism import power_users
from power_user_optimism import db_writers

def check_type_conversion(value_, type_):
    if not value_:
        raise ValueError("Expected something, that is convertible to type " +
              str(type_) + ", but None was provided")

    try:
        return type_(value_)
    except ValueError as e:
        print("Value error : expected simething, that is convertible to type " +
              str(type_) + ", but " + str(value_) + " was provided")

if __name__ == '__main__':
    load_dotenv("power_user_optimism/static_config.env")
    load_dotenv()

    # reading environmental variables
    with_public_data = (os.getenv("USE_PUBLIC_DATA") == "True")
    try:
        start_date = datetime.datetime.strptime(os.getenv("START_DATE"), "%d%m%Y")
    except TypeError as e:
        print(e)
        print("Environmental variable START_DATE is not set")
        sys.exit(1)
    except ValueError as e:
        print(e)
        print("Environmental variable START_DATE is" + os.getenv("START_DATE"))
        sys.exit(1)

    dates_range = check_type_conversion(os.getenv("DATES_RANGE"), int)
 
    if os.getenv("MONGO_HOST"):
        mongo_host = check_type_conversion(os.getenv("MONGO_HOST"), str)
    else:
        mongo_host = '127.0.0.1'

    if os.getenv("MONGO_PORT"):
        mongo_port = check_type_conversion(os.getenv("MONGO_PORT"), int)
    else:
        mongo_port = 27017

    mongo_database = check_type_conversion(os.getenv("MONGO_DATABASE"), str)
    
    bucket_name = check_type_conversion(os.getenv("METRONOMO_PUBLIC_DATA_BUCKET_NAME"), str)
    blob_name = check_type_conversion(os.getenv("METRONOMO_PUBLIC_DATA_BLOB_NAME"), str)

    target_contract = check_type_conversion(os.getenv("TARGET_CONTRACT"), str)
    quantile_ = check_type_conversion(os.getenv("QUANTILE"), float)
    window_ = check_type_conversion(os.getenv("WINDOW"), float)
    get_all_rfm_weights = check_type_conversion(os.getenv("GET_ALL_RFM_WEIGHTS"), bool)

    # generating dates rane
    dates = [start_date - datetime.timedelta(days=x) for x in range(dates_range)]
    print("Dates : " +  ",".join([str(d) for d in dates]))

    # creating connector to public Optimism data storage
    gcs_connector = dc.MetronomoTXCloudStorageConnector(dates, bucket_name, blob_name, with_public_data)

    # retrieving data
    data_ = gcs_connector.getData()
    print("Data loaded")

    # calculating powerUsers
    print("calculating powerUsers")
    powerUsers = power_users.getPowerUsers(data=data_, contract=target_contract, quantile=quantile_, window=window_, return_all=get_all_rfm_weights)

    print("calculated powerUsers : " + str(len(powerUsers)) + " entries")
    print(powerUsers.head())

    print("writing to mongo")

    mongo_writer = db_writers.MongoWriter(mongo_host, mongo_port)
    mongo_writer.writePowerUsersToCollection(powerUsers, mongo_database, collection=target_contract)

    print("finished writing to mongo")

    sys.exit()

