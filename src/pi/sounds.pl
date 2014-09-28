#!/usr/bin/env perl

while (<>) {
	chomp;
	if (($. % 5) == 0) {
		if ($_ eq "rest") {

		}
		elsif ($_ eq "waveIn") {
			`amixer -D pulse sset Master 5%+`;
		}
		elsif ($_ eq "waveOut") {
			`amixer -D pulse sset Master 5%-`;	
		}
		elsif ($_ eq "fist") {
			`amixer set master Mute`;
		}
		else {
			`amixer set master Unmute`;
		}
	}
}