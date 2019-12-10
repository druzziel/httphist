#!/usr/bin/python

################################
## Test harness for httphist  ##
################################

import unittest
import datetime
from httphist import get_dictionary, get_log_start_and_stop_times, filter_by_time

TMP_LOG_NAME = 'test_access.log'

def create_logfile():
    logtest = """78.136.44.21 - - [12/Mar/2017:03:14:02 +0000] "GET / HTTP/1.1" 200 24037 "-" "Iguana Monitoring/1.1 (https://monitoring.api.)"
50.57.61.5 - - [12/Mar/2017:03:14:37 +0000] "GET / HTTP/1.1" 200 24037 "-" "Iguana Monitoring/1.1 (https://monitoring.api.)"
50.56.142.171 - - [12/Mar/2017:03:14:44 +0000] "GET / HTTP/1.1" 200 24037 "-" "Iguana Monitoring/1.1 (https://monitoring.api.)"
78.136.44.21 - - [12/Mar/2017:03:15:01 +0000] "GET / HTTP/1.1" 200 24037 "-" "Iguana Monitoring/1.1 (https://monitoring.api.)"
146.185.205.43 - - [12/Mar/2017:03:15:25 +0000] "HEAD / HTTP/1.1" 200 - "http://topxxxdir.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.1144"
50.57.61.5 - - [12/Mar/2017:03:15:37 +0000] "GET / HTTP/1.1" 200 24037 "-" "Iguana Monitoring/1.1 (https://monitoring.api.)"
50.56.142.171 - - [12/Mar/2017:03:15:44 +0000] "GET / HTTP/1.1" 200 24037 "-" "Iguana Monitoring/1.1 (https://monitoring.api.)"
78.136.44.21 - - [12/Mar/2017:03:16:01 +0000] "GET / HTTP/1.1" 200 24037 "-" "Iguana Monitoring/1.1 (https://monitoring.api.)"
50.57.61.5 - - [12/Mar/2017:03:16:37 +0000] "GET / HTTP/1.1" 200 24037 "-" "Iguana Monitoring/1.1 (https://monitoring.api.)"
50.56.142.171 - - [12/Mar/2017:03:16:44 +0000] "GET / HTTP/1.1" 200 24037 "-" "Iguana Monitoring/1.1 (https://monitoring.api.)"
"""
    fp = open(TMP_LOG_NAME, 'w+')
    fp.write(logtest)
    fp.close()

class TestHttpHist(unittest.TestCase):
    
    def test_get_log_start_and_stop_times(self):
        controlStartTime = datetime.datetime(2017, 3, 12, 3, 14)
        controlEndTime   = datetime.datetime(2017, 3, 12, 3, 16)
        fp = open(TMP_LOG_NAME)
        sampleStartTime, sampleEndTime = get_log_start_and_stop_times(fp)
        fp.close()
        self.assertEqual(sampleStartTime, controlStartTime, "Checking start time equality")
        self.assertEqual(sampleEndTime, controlEndTime)

    def test_get_dictionary(self):

        controlStartTime = datetime.datetime(2017, 3, 12, 3, 14)
        controlEndTime   = datetime.datetime(2017, 3, 12, 3, 16)

        dictionary = get_dictionary(controlStartTime, controlEndTime)

        keys = dictionary.keys()
        keys.sort()
        sampleStartTime = keys[0]
        sampleEndtime = keys[-1]
        self.assertEqual(sampleStartTime, controlStartTime)
        self.assertEqual(sampleEndtime, controlEndTime)

    def test_filter_by_time(self):

        controlStartTime = datetime.datetime(2017, 3, 12, 1, 0)
        controlEndTime   = datetime.datetime(2017, 3, 12, 2, 0)

        grossStartTime = datetime.datetime(2017, 3, 12, 0, 0)
        grossEndTime   = datetime.datetime(2017, 3, 12, 3, 0)

        dictionary = get_dictionary(grossStartTime, grossEndTime)
        filtered_dictionary = filter_by_time(dictionary, controlStartTime, controlEndTime)

        keys = filtered_dictionary.keys()
        keys.sort()
        sampleStartTime = keys[0]
        sampleEndtime = keys[-1]
        self.assertEqual(sampleStartTime, controlStartTime)
        self.assertEqual(sampleEndtime, controlEndTime)


if __name__ == "__main__":

    create_logfile()
    unittest.main()
