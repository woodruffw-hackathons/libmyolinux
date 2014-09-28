#!/usr/bin/env perl

while (<>) {
	chomp;
	if (($. % 5) == 0) {
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
			print "fi\n";
		}
		else {
			#`amixer set master Unmute`;
		}
	}
}