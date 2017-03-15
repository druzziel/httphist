# httphist
Perl script for generating a histogram of requests per minute from common httpd logs


#!/usr/bin/env perl

sub print_hash {
        my $href = shift;
            print "$_\t=> $href->{$_}\n" for keys %{$href};
}
# log array that will store the processed lines of our log file
my %log;
 
while (<STDIN>) {

    # find the timestamp section of an httpd log
    if (/\[.*\]/) {
        my ($date, $hour, $minute, $seconds) = split(':', $&);
        my $fullTimestamp = join(':', ($date, $hour, $minute));
        if ( $log{$fullTimestamp} ) {
            $log{$fullTimestamp} += 1;
        } else {
            $log{$fullTimestamp} = 1;
        }
    }

}

# holy fuck this is nondeterministic
#while( my( $key, $val ) = each %log ) {
#    $val =~ s/ (\d+)$/"="x($1)/e ;
#    print "$key\t=>$val\n";
#}
my @output;

while( my( $key, $val ) = each %log ) {
    $val =~ s/(\d+)$/"="x($1)/e ;
    push @output, "$key\t$val\n";
}

# I'm a little uncomfortable with this because I don't understand it.
@output = 
    map $_->[0],
    sort { $a->[0] cmp $b->[0] }
    map  [ $_, join('', (split '/', $_)[2,1,0]) ], @output;
# end uncomfortable sort

foreach (@output) {
    print $_;
}
