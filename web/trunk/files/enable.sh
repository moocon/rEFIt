#!/bin/sh

if [ "$(uname -p)" != "i386" ]; then
  echo "You must run enable.sh on an Intel-based Macintosh!"
  exit 1
fi

if [ ! ( -f e.efi -o -f elilo.efi ) ]; then
  cd "`dirname "$0"`"
  if [ ! ( -f e.efi -o -f elilo.efi ) ]; then
    echo "You must run enable.sh from the directory where you put elilo"
    echo "or put enable.sh where elilo is!"
    exit 1
  fi
fi

if [ -f elilo.efi ]; then
  LOADERNAME=elilo.efi
else
  if [ -f e.efi ]; then
    LOADERNAME=e.efi
  fi
fi
LABELOPT=
if [ -f linux.vollabel ]; then
  LABELOPT="--labelfile linux.vollabel"
fi

set -x
sudo bless --folder . --file $LOADERNAME $LABELOPT
