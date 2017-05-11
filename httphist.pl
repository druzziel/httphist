#!/usr/bin/env perl

use strict;
use warnings;
use Data::Dumper;
# log array that will store the processed lines of our log file
my %log;

# lookup table
my %monthNumbers = qw(
	jan  1
	feb  2
	mar  3
	apr  4
	may  5
	jun  6
	jul  7
	aug  8
	sep  9
	oct  10
	nov  11
	dec  12
);


my $arg = "-scale";
 
my $scale = 1;
if ( grep( /^$arg$/, @ARGV ) ) {
    $scale = 3;
}

# Setup : I was looking for a clever way to fill in missing values in the output array
# so that it would be easier to spot patterns (including down time) in the output.
# Then I realized it would be easier to just start with all the possible values present.
sub dateTimeFromLogString {
	my $logstring = shift;
}

# Step One: Read in the input file and store the data in a hash.
while (<STDIN>) {

    # find the timestamp section of an httpd log
    if (/\[.*\]/) {
        my ($date, $hour, $minute, $seconds) = split(':', $&);
		$date =~ s/\[//;
		my ($day, $month, $year) = split('/', $date);
		$month = $monthNumbers{ lc substr($month, 0, 3)  };
        my $fullTimestamp = DateTime->new( year => $year,
			month => $month,
			day => $day,
			hour => $hour,
			minute => $minute);
        if ( $log{$fullTimestamp} ) {
            $log{$fullTimestamp} += 1;
        } else {
            $log{$fullTimestamp} = 1;
        }
    }

}

# Step Two: Put the records into an array so they can be sorted.
# Transform the hash's values from integers into a string of
# that many '=' characters.
my @output;

while( my( $key, $val ) = each %log ) {
    if ( $scale == 3 ) {
        $val =~ s/(\d+)$/"="x($1\/3)/e ;
    } else {
        $val =~ s/(\d+)$/"="x($1)/e ;
    }
	my $myString = "$key\t$val\n";
    push @output, $myString;
}

# Step Three: Sort the array.
# The intent here is to sort the records by date.
# Schwarzian transform sort http://stackoverflow.com/questions/2491471/how-can-i-sort-dates-in-perl
@output = 
    map $_->[0],
    sort { $a->[0] cmp $b->[0] }
    map  [ $_, join('', (split ':', $_)[2,1,0]) ], @output;


# Step Four: Insert the missing records.
use DateTime;
use DateTime::Duration;

sub getDateTimeFromRecord {
	my ($dateTimePart, $histo) = split '\t', shift;
	my ($datePart, $hour, $minute) = split ':', $dateTimePart;
	my ($day, $month, $year) = split '/', $datePart;
	$month = $monthNumbers{ lc substr($month, 0, 3)  };
	my $result = DateTime->new( year => $year,
			month => $month,
			day => $day,
			hour => $hour,
			minute => $minute);
	return $result;
}

# generate the next minute after the one passed in.
sub getNextDateTimeRecord {
	my $currentDateTime = shift;
	return $currentDateTime->add( DateTime::Duration->new(minutes => 1) );
}

sub getPreviousDateTimeRecord {
	my $currentDateTime = shift;
	return $currentDateTime->subtract( DateTime::Duration->new(minutes => 1) );
}

# date format in logs:
#[12/Mar/2017:03:14:02 +0000]

sub getLogLine {
	my $dt = shift;
	return sprintf( "%s/%s/%s:%s:%s", $dt->day, $dt->month, $dt->year, $dt->hour, $dt->minute);
}


#my $presentRecord;
#for my $i (0 .. ( scalar @output ) -2 ) {
#
#	my $j = $i + 1;
#	my $now = getDateTimeFromRecord( $output[$i] );
#	my $next = getDateTimeFromRecord( $output[$j] );
#	my $minute = DateTime::Duration->new(minutes => 1);
#	my $newRecord = getLogLine( getPreviousDateTimeRecord( getDateTimeFromRecord( $output[$j] ) ) );
#	until ( DateTime::Duration->compare( ( $next - $now ) , $minute ) == 0 ) {
#		splice @output, $j, 0, $newRecord;
#	}
#
#}

# Step Five: Print it.
foreach my $line ( @output ) {
	print $line;
}

