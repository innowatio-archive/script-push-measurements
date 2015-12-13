from datetime import timedelta
from itertools import chain

TYPES = ["activeEnergy", "maxPower", "reactiveEnergy"]
UNITS = ["kWh", "kW", "kVARh"]


def body_formatter(measurements):
	"""
				IN
	{
		'realeMeno1': 0.0,
		'contrattuale': 0.0,
		'realeMeno7': 0.0,
		'reale': 0.225,
		'tipologia': 3,
		'pod': 'IT001E00005045',
		'data': datetime.datetime(2015, 10, 18, 23, 0)
	}

				OUT
	{
	    "sensorId": "IT001E00030554",
	    "date": "2015-10-14T15:08:16.652Z",
	    "timeStep": 3600000,
	    "measurements": [
	        {
	            "type": "activeEnergy",
	            "source": "forecast",
	            "values": [59.5, null, null, 57.4, 59],
	            "unitOfMeasurement": "kWh"
	        },
	        {
	            "type": "reactiveEnergy",
	            "source": "forecast",
	            "values": [10.5, 11, 59],
	            "unitOfMeasurement": "kVARh"
	        },
	        {
	            "type": "maxPower",
	            "source": "forecast",
	            "values": [180, 186, null, 91],
	            "unitOfMeasurement": "kW"
	        }
	    ]
	}

	"""

	starting_date = measurements[0]["data"]

	res = {
		"sensorId": measurements[0]["pod"],
		"date": zuludate(starting_date),
		"timeStep": 3600000,
	}

	measuresArray = [{
        "type": "activeEnergy",
        "source": "reading",
        "values": [],
        "unitOfMeasurement": UNITS[0]
    },
    {
        "type": "maxPower",
        "source": "reading",
        "values": [],
        "unitOfMeasurement": UNITS[1]
    },
    {
        "type": "reactiveEnergy",
        "source": "reading",
        "values": [],
        "unitOfMeasurement": UNITS[2]
    }]

	for type in TYPES:
		index = TYPES.index(type)
		criteria = lambda m: m["tipologia"] is index +1
		submeasures = filter(criteria, measurements)
		last_date = starting_date - timedelta(hours=1)
		for meas in submeasures:
			measuresArray[index]["values"] += get_values(last_date, meas)
			last_date = meas["data"]

	res.update({"measurements": measuresArray})

	return res


def get_values(old_date, mes):
	res = []
	if (mes["data"] - old_date).total_seconds() / 3600 >= 1:
		res.append([None] * (int((mes["data"] - old_date).total_seconds() / 3600) -1))
	res.append([mes["reale"]])
	return list(chain.from_iterable(res))


def zuludate(date):
	# TODO: find a better way to get GMT+0 time
	return (date - timedelta(hours=1)).strftime("%Y-%m-%dT%X.000Z")
