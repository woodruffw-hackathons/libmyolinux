#!/usr/bin/env perl

my $lc = 0;
while (<>) {
	if ($lc % 5) {
		if ($_ eq "rest") {

		}
		elsif ($_ eq "waveIn") {
			#`amixer -D pulse sset Master 5%+`;
			print "wi\n";
		}
		elsif ($_ eq "waveOut") {
			#`amixer -D pulse sset Master 5%-`;
			print "wo\n";
		}
		elsif ($_ eq "fist") {
			#`amixer set master Mute`;
			print "fist\n";
		}
		else {
			#`amixer set master Unmute`;
		}
	}
	$lc++;

	if ($lc gt 2000000000) {
		$lc = 0;
	}
}