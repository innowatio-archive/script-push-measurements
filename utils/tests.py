from datetime import datetime, timedelta
import pusher_utils
import unittest

class TestPusherUtils(unittest.TestCase):

	def test_format_measurement(self):
		measurements = {
			"realeMeno1": 0.0,
			"contrattuale": 0.0,
			"realeMeno7": 0.0,
			"reale": 0.225,
			"tipologia": 3,
			"pod": "IT001E00005045",
			"data": datetime(2015, 10, 18, 0, 0)
		}

		self.assertEquals([0.225], pusher_utils.get_values(datetime(2015, 10, 18, 0, 0), measurements))

		# 1 hours difference: val
		measurements = {
			"realeMeno1": 0.0,
			"contrattuale": 0.0,
			"realeMeno7": 0.0,
			"reale": 0.225,
			"tipologia": 3,
			"pod": "IT001E00005045",
			"data": datetime(2015, 10, 18, 1, 0)
		}

		self.assertEquals([0.225], pusher_utils.get_values(datetime(2015, 10, 18, 0, 0), measurements))

		# 5 hours difference: None None None val
		measurements = {
			"realeMeno1": 0.0,
			"contrattuale": 0.0,
			"realeMeno7": 0.0,
			"reale": 0.225,
			"tipologia": 3,
			"pod": "IT001E00005045",
			"data": datetime(2015, 10, 18, 5, 0)
		}

		self.assertEquals([None, None, None, None, 0.225], pusher_utils.get_values(datetime(2015, 10, 18, 0, 0), measurements))


	def test_zuludate(self):
		date = datetime(2015, 10, 14, 16, 8, 16, 652)
		expected = "2015-10-14T15:08:16.000Z"
		self.assertEquals(expected, pusher_utils.zuludate(date))


	def test_body_formatter(self):
		self.maxDiff = None

		measurements = [{
			"realeMeno1": 0.0,
			"contrattuale": 0.0,
			"realeMeno7": 0.0,
			"reale": 1,
			"tipologia": 1,
			"pod": "IT001E00005045",
			"data": datetime(2015, 1, 1, 1, 0)
		},
		{
			"realeMeno1": 0.0,
			"contrattuale": 0.0,
			"realeMeno7": 0.0,
			"reale": 3,
			"tipologia": 2,
			"pod": "IT001E00005045",
			"data": datetime(2015, 1, 1, 1, 0)
		},
		{
			"realeMeno1": 0.0,
			"contrattuale": 0.0,
			"realeMeno7": 0.0,
			"reale": 6,
			"tipologia": 1,
			"pod": "IT001E00005045",
			"data": datetime(2015, 1, 1, 2, 0)
		},
		{
			"realeMeno1": 0.0,
			"contrattuale": 0.0,
			"realeMeno7": 0.0,
			"reale": 5,
			"tipologia": 3,
			"pod": "IT001E00005045",
			"data": datetime(2015, 1, 1, 2, 0)
		},
		{
			"realeMeno1": 0.0,
			"contrattuale": 0.0,
			"realeMeno7": 0.0,
			"reale": 15,
			"tipologia": 2,
			"pod": "IT001E00005045",
			"data": datetime(2015, 1, 1, 4, 0)
		}]

		expected = {
			"date": "2015-01-01T00:00:00.000Z",
			"sensorId": "IT001E00005045",
			"measurements": [{
				"values":[1, 6],
				"source": "reading",
				"type": "activeEnergy",
				"unitOfMeasurement": "kWh"
			},{
				"values":[3, None, None, 15],
				"source": "reading",
				"type": "maxPower",
				"unitOfMeasurement": "kW"
			},{
				"values":[None, 5],
				"source": "reading",
				"type": "reactiveEnergy",
				"unitOfMeasurement": "kVARh"
			}],
			"timeStep": 3600000
		}

		self.assertEquals(expected, pusher_utils.body_formatter(measurements))

if __name__ == "__main__":
    unittest.main()