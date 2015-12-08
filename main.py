from datetime import datetime
import os
import logging
import pymssql
import requests
import utils.pusher_utils as utils


MSSQL_SERVER = os.environ["MSSQL_SERVER"]
MSSQL_DB = os.environ["MSSQL_DB"]
MSSQL_USER = os.environ["MSSQL_USER"]
MSSQL_PASSWORD = os.environ["MSSQL_PASSWORD"]
API_URL = os.environ["API_URL"]
LOG_DIR = "logs/"


def get_mssql_connection():
    return pymssql.connect(
    	MSSQL_SERVER,
    	MSSQL_USER,
    	MSSQL_PASSWORD,
    	MSSQL_DB)

def get_misure(cursor, pod):
	str_now = datetime.now().strftime("%Y-%m-%d")
	query = "SELECT * FROM DatiReali WHERE pod=\'"+ pod +"\' AND data < \'"+ str_now +"\' AND data > \'2015-01-01\' ORDER BY data ASC"
	cursor.execute(query)
	return cursor

def get_recent_pods(cursor):
    cursor.execute("SELECT distinct(pod) as Codice FROM DatiReali where Data > '2014-01-01'")
    return cursor

def setup_logging():
	if not os.path.exists(LOG_DIR):
		os.makedirs(LOG_DIR)

	logging.basicConfig(
		filename=LOG_DIR + "push.log",
		format='%(asctime)s : %(levelname)s : %(message)s',
		datefmt='%m/%d/%Y %I:%M:%S %p', 
		level=logging.DEBUG)

def __main__():

	setup_logging()

	# Load data from DB
	connMSSQL = get_mssql_connection()
	cursorMSSQL = connMSSQL.cursor(as_dict=True)

	pods = get_recent_pods(cursorMSSQL).fetchall()
	print "found {} pods".format(len(pods))

	for pod in pods:
		podId = pod["Codice"]
		misure = (get_misure(cursorMSSQL, podId)).fetchall()

		if len(misure) > 0:
			print "-------------------- " + podId
			data = utils.body_formatter(misure)

			# Push
			r = requests.post(API_URL, data=data, verify=False)
			print "{} push result => {}".format(podId, r.status_code)
			logging.info("{} push result => {}".format(podId, r.status_code))
			if r.status_code > 300:
				print "Server message: " + r.text
				logging.error(r.text)
		else:
			print podId + " nothing to push"
			logging.info(podId + " nothing to push")


if __name__ == "__main__":
    __main__()
