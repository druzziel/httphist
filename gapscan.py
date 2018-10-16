#!/usr/bin/env python

import datetime,time,sys

TIME_FORMAT = '%d/%b/%Y:%H:%M'
apache_timestamp = '15/Oct/2018:15:59'
one_minute_delta = datetime.timedelta( minutes = 1 )

def convert_timestamp(apache_timestamp):
    """convert an Apache datetime string to a Python datetime object"""
    try:
        time_obj = datetime.datetime.strptime( apache_timestamp, TIME_FORMAT )
    except:
        raise TypeError, "%s is not a timestamp I recognize." % apache_timestamp
    return time_obj

def increment_timestamp( time_obj ):
    """returns a datetime object that is one minute ahead of the input object"""
    try:
        new_time_obj = time_obj + one_minute_delta
    except:
        raise TypeError, "%s is not a time object I recognize." % time_obj
    return new_time_obj

def print_output_line( bits ):
    """pretty-print a line of output"""
    time_obj = bits[1].strftime( TIME_FORMAT )
    print "%4s  %s" % ( bits[0], time_obj )

def extract_time( input_line ):
    """Takes a line from the input file and returns a time object based on that line's timestamp"""
    bits = input_line.split()
    apache_timestamp = bits[1]
    return convert_timestamp( apache_timestamp )

def compare_times( time_obj1, time_obj2 ):
    """returns True iff time_obj1 is one minute before time_obj2"""
    if time_obj1 + one_minute_delta == time_obj2:
        return True
    else:
        return False

if __name__ == "__main__":

    filename = sys.argv[1]

    fp = open(filename)
    lines = fp.readlines()
    fp.close()
    for x in range(1, len(lines) ):
            lastline = lines[x -1].strip()
            thisline = lines[x].strip()
            lasttime = extract_time( lastline )
            thistime = extract_time( thisline )
            bits = lastline.split()
            time_obj = convert_timestamp( bits[1] )
            print_output_line( (bits[0], time_obj) )
            while not compare_times( lasttime, thistime ):
                lasttime = increment_timestamp( lasttime )
                print_output_line( (0, lasttime) )
