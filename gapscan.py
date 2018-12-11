#!/usr/bin/env python

import datetime,time,sys
from subprocess import check_output

TIME_FORMAT = '%d/%b/%Y:%H:%M'
apache_timestamp = '15/Oct/2018:15:59'
one_minute_delta = datetime.timedelta( minutes = 1 )
DEBUG=False

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

def usage():
    print """usage: %s <logfile>
Where <logfile> is an Apache combined log.""" % sys.argv[0]

if __name__ == "__main__":

    if len(sys.argv) == 1:
        usage()
        sys.exit()


    filename = sys.argv[1]
    ncsa_timestamp_regex = "[0-9]+/[A-Z][a-z]+/[0-9]{4}:[0-9]{2}:[0-9]{2}:[0-9]{2}(.*?\])"
    search_command="egrep -o '" + ncsa_timestamp_regex + "' " + filename + " | cut -d\: -f1-3 | tr -d \[ | sort | uniq -c"
    lines = check_output(search_command, shell=True).split('\n')
    if DEBUG:
        fp = open("debug.txt", 'w')
        fp.write("%s\n" % search_command)
        fp.write("%s" % lines)
        fp.close()
    for x in range(1, len(lines) ):
        lastline = lines[x -1].strip()
        thisline = lines[x].strip()
        lasttime = extract_time( lastline )
        # if this is a blank line, ignore it and fill it in
        # with the next sequential timestamp
        if len(thisline) == 0:
            thistime = increment_timestamp( lasttime )
        else:
            thistime = extract_time( thisline )
        print_output_line( (lastline.split()[0], lasttime) )
        while not compare_times( lasttime, thistime ):
            lasttime = increment_timestamp( lasttime )
            print_output_line( (0, lasttime) )
