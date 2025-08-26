#!/usr/bin/perl

use CGI;
use Math::Trig;
use strict;
use utf8;
use open qw(:std :encoding(UTF-8));



$| = 1;



# Fetch posted data
my $cgi = CGI->new;
my %PARG;
foreach my $i ($cgi->param) {
	$PARG{$i} = $cgi->param($i);	
}
	
	
	
# Set default html-field values
my $val_orient = '[1,0,0,0]';
my $val_q1 = '1';
my $val_q2 = '0';
my $val_q3 = '0';
my $val_q4 = '0';
my $val_rz = '0';
my $val_ry = '0';
my $val_rx = '0';
my $val_rz_rad = '0';
my $val_ry_rad = '0';
my $val_rx_rad = '0';



# Check if user has posted valid data
if ($PARG{orient}) {
	# User posted ORIENT data
	$val_orient = lc($PARG{orient});
	($val_q1, $val_q2, $val_q3, $val_q4) = orient2quat($val_orient);
	($val_rz, $val_ry, $val_rx) = quat2euler($val_q1, $val_q2, $val_q3, $val_q4);
	($val_rz_rad, $val_ry_rad, $val_rx_rad) = deg2rad3($val_rz, $val_ry, $val_rx);

} elsif (($PARG{q1}) || ($PARG{q2}) || ($PARG{q3}) || ($PARG{q4})) {
	# User posted QUATERNIONS data
	$val_q1 = $PARG{q1};
	$val_q2 = $PARG{q2};
	$val_q3 = $PARG{q3};
	$val_q4 = $PARG{q4};
	$val_orient = '[' . $val_q1 . ',' . $val_q2 . ',' . $val_q3 . ',' . $val_q4 . ']';
	($val_rz, $val_ry, $val_rx) = quat2euler($val_q1, $val_q2, $val_q3, $val_q4);
	($val_rz_rad, $val_ry_rad, $val_rx_rad) = deg2rad3($val_rz, $val_ry, $val_rx);
	
} elsif (($PARG{rz}) || ($PARG{ry}) || ($PARG{rx})) {
	# User posted ROTATION ANGLES data
	$val_rz = $PARG{rz};
	$val_ry = $PARG{ry};
	$val_rx = $PARG{rx};
	($val_q1, $val_q2, $val_q3, $val_q4) = euler2quat($val_rz, $val_ry, $val_rx);
	$val_orient = '[' . $val_q1 . ',' . $val_q2 . ',' . $val_q3 . ',' . $val_q4 . ']';
	($val_rz_rad, $val_ry_rad, $val_rx_rad) = deg2rad3($val_rz, $val_ry, $val_rx);
	
} elsif (($PARG{rz_rad}) || ($PARG{ry_rad}) || ($PARG{rx_rad})) {
	# User posted ROTATION ANGLES RADIANS data
	$val_rz_rad = $PARG{rz_rad};
	$val_ry_rad = $PARG{ry_rad};
	$val_rx_rad = $PARG{rx_rad};
	($val_rz, $val_ry, $val_rx) = rad2deg3($val_rz_rad, $val_ry_rad, $val_rx_rad);
	($val_q1, $val_q2, $val_q3, $val_q4) = euler2quat($val_rz, $val_ry, $val_rx);
	$val_orient = '[' . $val_q1 . ',' . $val_q2 . ',' . $val_q3 . ',' . $val_q4 . ']';

}
my $val_sqsum = quat2sqsum($val_q1, $val_q2, $val_q3, $val_q4);



# Generate webpage
print <<EOM;
content-type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>OrientCalc</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<h1>OrientCalc</h1>

<form method="post" action="index.cgi">
<table>
<tr><td class="label">Orient</td><td><input type="text" name="orient" value="$val_orient" size="100"> <input type="submit" value="Submit"></td></tr>
<tr><td class="label">SquareSum</td><td>$val_sqsum
EOM
if (abs(1 - $val_sqsum) < 0.00001) {
	print '<span style="color: #00bb00; font-weight: bold;">OK</span>';
} elsif (abs(1 - $val_sqsum) < 0.1) {
	print '<span style="color: #bbbb00; font-weight: bold;">Slightly un-normalized, consider using NOrient() to fix.</span></font>';
} else {
	print '<span style="color: #bb0000; font-weight: bold;">Unusable</span></font>';
}
print <<EOM;
</td></tr>
</table>
</form>

<form method="post" action="index.cgi">
<table>
<tr><td class="label">Q1 (w)</td><td><input type="text" name="q1" value="$val_q1"></td></tr>
<tr><td class="label">Q2 (x)</td><td><input type="text" name="q2" value="$val_q2"></td></tr>
<tr><td class="label">Q3 (y)</td><td><input type="text" name="q3" value="$val_q3"></td></tr>
<tr><td class="label">Q4 (z)</td><td><input type="text" name="q4" value="$val_q4"> <input type="submit" value="Submit"></td></tr>
</table>
</form>
<form method="post" action="index.cgi">
<table>
<tr><td colspan="2">Degrees (ZYX Order)</td></tr>
<tr><td class="label">Rz</td><td><input type="text" name="rz" value="$val_rz"></td></tr>
<tr><td class="label">Ry</td><td><input type="text" name="ry" value="$val_ry"></td></tr>
<tr><td class="label">Rx</td><td><input type="text" name="rx" value="$val_rx"> <input type="submit" value="Submit"></td></tr>
</table>
</form>
<form method="post" action="index.cgi">
<table>
<tr><td colspan="2">Radians (ZYX Order)</td></tr>
<tr><td class="label">Rz</td><td><input type="text" name="rz_rad" value="$val_rz_rad"></td></tr>
<tr><td class="label">Ry</td><td><input type="text" name="ry_rad" value="$val_ry_rad"></td></tr>
<tr><td class="label">Rx</td><td><input type="text" name="rx_rad" value="$val_rx_rad"> <input type="submit" value="Submit"></td></tr>
</table>
</form>
<form method="post" action="index.cgi">
<table>
<tr><td><input type="submit" value="Reset"></td></tr>
</table>
</form>
EOM

# COUNTER
open(my $FILE, '<', 'counter.txt');
my $counter = <$FILE>;
close($FILE);
$counter++;
if ($counter > 10) {
	open(my $FILE, '>', 'counter.txt');
	print $FILE $counter;
	close($FILE);
}

print <<EOM;
<p>Served: $counter</p>
<p><i><small><a href="http://www.straumland.com">www.straumland.com</a></small></i></p>
</body>
</html>
EOM



# Logfile for debugging
open(my $FILE, '>>stats.log');
print $FILE $ENV{REMOTE_ADDR} . ';' . $ENV{HTTP_REFERER} . ';' . $ENV{HTTP_USER_AGENT} . ';' . $ENV{REQUEST_URI} . ';' . "\n";
close($FILE);
if ((-s 'stats.log') > 1000000) {
	unlink('stats2.log');
	rename('stats.log', 'stats2.log');
}



exit;



sub orient2quat {
	my($orient) = @_;
	
	# Convert Orient datatype to four quaternion values
	
	# Set default values
	my $q1 = 1;
	my $q2 = 0;
	my $q3 = 0;
	my $q4 = 0;

	# Use regexp to find values
	if ($orient =~ /\[([\d\-\+e\.]+),([\d\-\+e\.]+),([\d\-\+e\.]+),([\d\-\+e\.]+)\]/i) {
		# If regexp was found, replace default values, and limit decimal digit count
		$q1 = maxdec($1, 10);
		$q2 = maxdec($2, 10);
		$q3 = maxdec($3, 10);
		$q4 = maxdec($4, 10);
	}
	
	return($q1, $q2, $q3, $q4);
}



sub euler2quat {
	my($rz, $ry, $rx) = @_;

	# Convert 3 deg angles to 4 quaternion values

	# To radians
	my($rz_rad, $ry_rad, $rx_rad) = deg2rad3($rz, $ry, $rx);

	# To Quaternions
	my $toq_cy = cos($rz_rad * 0.5);
	my $toq_sy = sin($rz_rad * 0.5);
	my $toq_cp = cos($ry_rad * 0.5);
	my $toq_sp = sin($ry_rad * 0.5);
	my $toq_cr = cos($rx_rad * 0.5);
	my $toq_sr = sin($rx_rad * 0.5);
	
	my $q1 = ($toq_cr * $toq_cp * $toq_cy) + ($toq_sr * $toq_sp * $toq_sy);
	my $multiplier = $q1 >= 0 ? 1 : -1;
	
	$q1 = (($toq_cr * $toq_cp * $toq_cy) + ($toq_sr * $toq_sp * $toq_sy)) * $multiplier;
	my $q2 = (($toq_sr * $toq_cp * $toq_cy) - ($toq_cr * $toq_sp * $toq_sy)) * $multiplier;
	my $q3 = (($toq_cr * $toq_sp * $toq_cy) + ($toq_sr * $toq_cp * $toq_sy)) * $multiplier;
	my $q4 = (($toq_cr * $toq_cp * $toq_sy) - ($toq_sr * $toq_sp * $toq_cy)) * $multiplier;
	
	# Return with limited decimal digit count
	return(maxdec($q1, 10), maxdec($q2, 10), maxdec($q3, 10), maxdec($q4, 10));
}



sub quat2euler {
	my($q1, $q2, $q3, $q4) = @_;
	
	# Calculate deg euler angles to quaternions
	# using rotational order used in ABB robotics quaternions (ZYX).
	
	# Rotation around X axis
	my $sinr_cosp = 2 * (($q1 * $q2) + ($q3 * $q4));
	my $cosr_cosp = 1 - (2 * (($q2 ** 2) + ($q3 ** 2)));
	my $rx = atan2($sinr_cosp, $cosr_cosp);
	
	# Rotation around Y axis
	my $sinp = 2 * (($q1 * $q3) - ($q4 * $q2));
	my $ry = abs($sinp) >= 1 ? copysign(pi / 2, $sinp) : asin($sinp);
	
	# Rotation around Z axis
	my $siny_cosp = 2 * (($q1 * $q4) + ($q2 * $q3));
	my $cosy_cosp = 1 - (2 * (($q3 ** 2) + ($q4 ** 2)));
	my $rz = atan2($siny_cosp, $cosy_cosp);

	# Convert from radians to deg and return results
	return(rad2deg1($rz), rad2deg1($ry), rad2deg1($rx));
}



sub deg2rad3 {
	my($rz, $ry, $rx) = @_;
	return(deg2rad1($rz), deg2rad1($ry), deg2rad1($rx));
}



sub deg2rad1 {
	my($deg) = @_;
	return($deg * (2 * pi) / 360);
}



sub rad2deg3 {
	my($rz, $ry, $rx) = @_;
	return(rad2deg1($rz), rad2deg1($ry), rad2deg1($rx));
}



sub rad2deg1 {
	my($rad) = @_;
	return($rad * 360 / (2 * pi));
}



sub quat2sqsum {
	my($q1, $q2, $q3, $q4) = @_;
	return(abs(sqrt(($q1 * $q1) + ($q2 * $q2) + ($q3 * $q3) + ($q4 * $q4))));
}



sub maxdec {
	my($val, $dec) = @_;
	return(int($val * (10 ** $dec)) / (10 ** $dec));
}



sub copysign {
	my($val1, $val2) = @_;
	return($val2 >= 0 ? abs($val1) : -abs($val1));
}


