#!/bin/sh

# Get submission of this work.
work=a1

coursedir=$HOME/120
submitdir=/primula/Courses/submit/csca20s/submit
# submissions get copied to studir from the submit directory
studir=$coursedir/assts/$work/submit

mkdir $studir
for login in `ls $submitdir`
  do 
  if [ -d $submitdir/$login/$work ]
      then
      if [ ! -d $studir/$login ]
	  then
	  mkdir $studir/$login
      fi
      cp -R $submitdir/$login/$work $studir/$login
  fi
done
