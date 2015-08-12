set title "Test"
set key invert reverse Left outside
set key autotitle columnheader
set style data histogram
set style histogram rowstacked
set style fill solid border -1
set boxwidth 0.75
plot "sum.txt" u 2:xtic(1) t 'Swim','' u 3 t 'Bike','' u 4 t 'Run'

