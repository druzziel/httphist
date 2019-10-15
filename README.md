# httphist
Python script for generating a histogram of requests per minute from common httpd logs

# Usage

	httphist [-h] [-s SCALING_FACTOR] [-a] [-c COLUMNS] logfile


Where access.log has the Apache common log format, e.g.:

    78.136.44.21 - - [12/Mar/2017:03:14:02 +0000] "GET / HTTP/1.1" 200 24037 "-" "Iguana Monitoring/1.1 (https://monitoring.api.)"
    50.57.61.5 - - [12/Mar/2017:03:14:37 +0000] "GET / HTTP/1.1" 200 24037 "-" "Iguana Monitoring/1.1 (https://monitoring.api.)"
    50.56.142.171 - - [12/Mar/2017:03:14:44 +0000] "GET / HTTP/1.1" 200 24037 "-" "Iguana Monitoring/1.1 (https://monitoring.api.)"
    78.136.44.21 - - [12/Mar/2017:03:15:01 +0000] "GET / HTTP/1.1" 200 24037 "-" "Iguana Monitoring/1.1 (https://monitoring.api.)"
    146.185.205.43 - - [12/Mar/2017:03:15:25 +0000] "HEAD / HTTP/1.1" 200 - "http://topxxxdir.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.1144"
    50.57.61.5 - - [12/Mar/2017:03:15:37 +0000] "GET / HTTP/1.1" 200 24037 "-" "Iguana Monitoring/1.1 (https://monitoring.api.)"
    50.56.142.171 - - [12/Mar/2017:03:15:44 +0000] "GET / HTTP/1.1" 200 24037 "-" "Iguana Monitoring/1.1 (https://monitoring.api.)"
    78.136.44.21 - - [12/Mar/2017:03:16:01 +0000] "GET / HTTP/1.1" 200 24037 "-" "Iguana Monitoring/1.1 (https://monitoring.api.)"
    50.57.61.5 - - [12/Mar/2017:03:16:37 +0000] "GET / HTTP/1.1" 200 24037 "-" "Iguana Monitoring/1.1 (https://monitoring.api.)"
    50.56.142.171 - - [12/Mar/2017:03:16:44 +0000] "GET / HTTP/1.1" 200 24037 "-" "Iguana Monitoring/1.1 (https://monitoring.api.)"

And scaling factor is a number used to shorten the historgram lines in output.
Use the -a (--autoscale) flag to automatically scale the histogram lines down to an optional COLUMNS width.
If -c (--columns, --cols) is not provided, COLUMNS defaults to 60.

# Output

	2017-03-12 03:14:00    3 ###
	2017-03-12 03:15:00    4 ####
	2017-03-12 03:16:00    3 ###
