import sys
import os
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def connect_to_mongodb():
    import urllib.parse

    # don't do for macos
    # possibly we should use direct mongo uri defined in the enviroment rather than username and password it could give us encoding issue
    # but commenting out the user name one if we want we can do it later as well
    if sys.platform != "darwin":
        # If localhost fails, try the Kubernetes service
        # username = urllib.parse.quote_plus(os.environ.get("MONGO_INITDB_ROOT_USERNAME"))
        # password = urllib.parse.quote_plus(os.environ.get("MONGO_INITDB_ROOT_PASSWORD"))
        # port = os.environ.get("MONGO_PORT", "27017")
        # if not username or not password:
            # logger.error("No username and password found in the enviroment or secrets")
        try:
            uri = os.getenv("MONGODB_URL")
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            client.admin.command("ismaster")
            logging.debug("Connected to MongoDB on Kubernetes service")
            return client
        except ConnectionFailure:
            logging.debug("Failed to connect to MongoDB on Kubernetes service")

    # First, try to connect to localhost
    try:
        client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=5000)
        # The ismaster command is cheap and does not require auth.
        client.admin.command("ismaster")
        logging.debug("Connected to MongoDB on localhost")
        return client
    except ConnectionFailure:
        logging.debug(
            "Failed to connect to MongoDB on localhost. Trying Kubernetes service..."
        )

    # If both attempts fail, raise an exception
    raise ConnectionFailure(
        "Could not connect to MongoDB on localhost or Kubernetes service"
    )