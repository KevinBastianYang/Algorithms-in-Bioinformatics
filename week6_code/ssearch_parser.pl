#!/usr/bin/perl -w
use strict;

my ($ssearch_out) = @ARGV;
my $usage = "This script is to get the best hit from ssearch output file with 1 input sequence.
usage: $0 <ssearch_output_file>
";
die $usage if @ARGV<1;

open(SSOUT,$ssearch_out)||die("open $ssearch_out error!\n");

my $query = "";
my $hit = "";
my $Z_score = "";
my $E_score = "";

my $flag = 0;
while(<SSOUT>){
    chomp;
    if($flag == 0)
    {
		if(/^Query:\s*(\w+)/) { $query = $1;}
		elsif(/^The best scores are:/)  {$flag = 1;}
		else  {next;}
    }
    elsif($flag == 1)
    {
		if(/^(?<hit_name>[\w\.\-]+)\s+.+\s+(?<Escore>[0-9e\-\.]+)$/)
		{
	    	$hit = $+{hit_name};
	    	$E_score = $+{Escore};
	    	$flag = 2;
		}
		else { next;}
    }
    elsif($flag == 2)
    {
    	if(/^>>$hit/) {$flag = 3;}
    	else {next;}
    }
    elsif($flag == 3)
    {
    	if(/^.+Z\-score:\s+([0-9\.]+)/) 
    	{
    		$Z_score = $1;
    		last;
    	}
    	else {next;}

    }
}

close SSOUT;

print "Best hit to $query is: $hit, with E-score $E_score, Z-score $Z_score.\n";

exit;
