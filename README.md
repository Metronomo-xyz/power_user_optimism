# power_user_optimism
Tool to find most valuable users of given smart_contract address on Optimism blockchain

This module calculates users value score based on usage metrics of given smart contract and stores users with their scores to provided MongoDB database.

After that, you can use most valuable users of given smart contract to create a list of users across whole network, who might be very similar and worth interacting with them (by airdrops, ads etc.). To find similar users use [user_similarity_optimism tools](https://github.com/Metronomo-xyz/user_similarity_optimism_calculator) from our repositories.

Module relies on RMF (but withoun monetary part) analysis.
 - module calculates RF score for all users
 - then module defines given quantile of score
 - then module consider all the users with score higher then quantile as most valuable users (power users)

## Prerequisites

### Hardware
#### Calculation server
The main bottleneck of current module is RAM, so at least 4GB of RAM needed. 

#### MongoDB Server
Any kind of preferred infrastructure for MongoDB server is possible. At least 1 GB of available disk space needed. Better to have 20GB or more of available disk space.

### Data source
Either you can use provided public transactions data or use your own data connector. 

To use public data user environmental variable `USE_PUBLIC_DATE` in `static_config.env`

To use your own data connector you have to implement DataConnector abstract class and provided some setting in config file (if needed). 

### Run MongoDB server

To store power users and their scores module use MongoDB. 

You have to run MongoDB server and provide its host, port, database and collection to the module in `.env` file

## Running from Docker image
It's the easiest way to run the module

### 1. Create .env file

Copy `.env` file from `https://github.com/Metronomo-xyz/power_user_optimism`

Put it on your machine

Change values in .env file like described [below](#env)

### 2. Pull image from docker

```
sudo docker pull randromtk/power_user_optimism:dev
```

### 3. Run docker container

```
sudo docker run -it --env-file <path to .env file> <image tag>
```

- `<path to .env file>` - path to file, that you created [before](#1createenvfile)
- `<image tag>` - image tag. Might be obtained by running `sudo docker images` command, in our example is "randromtk/power_user_optimism:dev"

*To run locally (but this works only for Linux)*

```
sudo docker run -it --env-file <path to env file with local mongo host> --network="host" <image tag>
```

example:
```
sudo docker run -it --env-file .env --network="host" randromtk/power_user_optimism:dev
```

## Running from the source code

### 0. Clone repository

`git clone https://github.com/Metronomo-xyz/power_user_optimism.git`

### 1. Create virtual environment

It's recommended to use virtual environment while using module

If you don't have `venv` installed run (ex. for Ubuntu)
```
sudo apt-get install python3-venv
```
then create and activate virtual environment
```
python3 -m venv power_user_optimism
source power_user_optimism/bin/activate
```

### 2. Install requirements
Run
```
pip install -r power_user_optimism/requirements.txt
```

### 3. Set environmental variables

env-files:
- [.env](#env) - Need to take file from current repository as example, change it, and keep it in module directory (in the same directory as `__main__.py`)
- [static_config.env](#static_configenv) - better not to change

#### .env
Flag to use publicly available Optimism blockchain data.
```
 - USE_PUBLIC_DATA
# If `True` data from Metronomo public bucket will be used
# If `False` - you have to write your own class to get the data from your own storage 
 ```
For public data START_DATE and DATES_RANGE variables do nothing - data will be taken from static source. We update this example data from time to time, but not regularly.

Variables to access MongoDB server. You HAVE to set your own

```
- MONGO_HOST - host of mongodb server to store power users data
- MONGO_PORT - port of mongodb server  to store power users data
- MONGO_DATABASE  - mongo database name to store power users data
```
Variables to define which contract to analyze and how
```
TARGET_CONTRACT - the contract users of which will be analysed.
QUANTILE - quantile of value score above which user will be considered as most valuable (power users). Default = 0.95
WINDOW - window of dates (in number of days) to calculate value score.
GET_ALL_RFM_WEIGHTS - if True then value score of ALL users of target smart contract inside the window will be stored in Mongo. Significantly increase ammoun of data stored in MongoDB. Use with caution.
```

Dates choosing. You might use any START_DATE and DATE_RANGE as you want
```
- START_DATE - the last date of the dates period in `ddmmyyyy` format
- DATES_RANGE - number of days to take into power users calculation. For example, if start date is 12122022 and range 30 then dates will be since 13-11-2022 to 12-12-2022 inclusively
```

#### static_config.env
Config file with environment variables to get public Optimism data from Metronomo cloud storage. DO NOT CHANGE
```
- METRONOMO_PUBLIC_DATA_PROJECT - name of the Google Cloud Storage project with public data
- METRONOMO_PUBLIC_DATA_BUCKET_NAME - name of the bucket with public data
- METRONOMO_PUBLIC_DATA_BLOB_NAME - name of the bucket with public data
```
We update this example data from time to time, but not regularly.

### 4. Run the module

```python3 -m power_user_optimism```

Power users and their scores will be stored in MongoDB on host, port provided in .env, in database and collections equal to the target_contract address
