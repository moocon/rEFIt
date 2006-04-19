#!/usr/bin/perl

use File::Find;
$| = 1;

sub convert_file {
  my $filename = shift;
  my $tmpfilename = "$filename.tmp";

  open(IN, $filename) or die "Can't read $filename: $!";
  open(OUT, ">".$tmpfilename) or die "Can't write $tmpfilename: $!";
  while (<IN>) {
    chomp;
    s/\r$//;
    $_ .= "\n";
    print OUT $_;
  }
  close(OUT) or die "Can't write $tmpfilename: $!";
  close(IN);

  rename($tmpfilename, $filename) or die "Can't move $tmpfilename to $filename: $!";

  # TODO: in the future, do the convert in memory and check if anything has
  #  changed; don't touch the file unless necessary
}

sub find_filter {
  if (-f and /\.([chs]|txt)$/i) {
    &convert_file($_);
  }
}


if ($#ARGV >= 0) {
  foreach $filename (@ARGV) {
    if (-f $filename) {
      &convert_file($filename);
    } elsif (-d $filename) {
      find(\&find_filter, $filename);
    }
  }
} else {
  find(\&find_filter, ".");
}

exit 0;
