set grid

set xlabel "Time (s)"
set ylabel "Supply Current (A)"

unset logscale x
unset logscale y

set format y "%g"
set format x "%g"

plot '10201.data' using 1:(-1*$2) with lines lw 2 title ""

set terminal push
set terminal postscript eps color
set out '10201_inverted.eps'

replot
