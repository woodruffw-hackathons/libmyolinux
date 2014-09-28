#!/usr/bin/env perl

my $lc = 0;
while (<>) {
	if ($lc % 5) {
		if ($_ eq "rest") {
			continue;
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
	$lc++;

	if ($lc gt 2000000000) {
		$lc = 0;
	}
}