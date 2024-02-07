reset

# png
set terminal pngcairo dashed size 1000,800 enhanced font "Verdana,30"
#set terminal pngcairo dashed size 2500,1750 enhanced font "Verdana,50"
# dashed option enables dashed linestyle in pngcairo

# Custom line styles

LW1= 0.0
LW2 = 0.0
PS = 1

set style line 1 lt 1 pt 7 ps PS lw LW1 lc rgb '#0072bd' # blue
set style line 2 lt 1 pt 7 ps PS lw LW1 lc rgb '#d95319' # orange
set style line 3 lt 1 pt 7 ps PS lw LW1 lc rgb '#edb120' # yellow
set style line 4 lt 1 pt 7 ps PS lw LW1 lc rgb '#7e2f8e' # purple
set style line 5 lt 1 pt 7 ps PS lw LW1 lc rgb '#77ac30' # green
set style line 6 lt 1 pt 7 ps PS lw LW1 lc rgb '#4dbeee' # light-blue
set style line 7 lt 1 pt 7 ps PS lw LW1 lc rgb '#a2142f' # red
set style line 8 lt 1 pt 7 ps PS lw LW1 lc rgb '#666666' # grey
set style line 9 lt 1 pt 7 ps PS lw LW1 lc rgb '#99ae52' # olive
set style line 10 lt 1 pt 7 ps PS lw LW1 lc rgb '#000000' # black

set style line 102 lc rgb '#808080' lt 0 lw 3
set grid back ls 102

# Set the border using the linestyle 80 that we defined
# 3 = 1 + 2 (1 = plot the bottom line and 2 = plot the left line)
# back means the border should be behind anything else drawn
# set style line 80 lt 0 lw 3 lc rgb "#808080"
# set border 3 back ls 80

# MACROS
# x- and ytics for each row resp. column
NOXTICS = "set xtics ('' 0, '' 0.4, '' 0.8, '' 1.2); \
          unset xlabel; \
          set mxtics 2 "
XTICS = "set xtics 0, 0.2, 1.6; \
          set xlabel 'RMSD (Å)' offset 0,0.4; \
          set mxtics 2"
NOYTICS = " set ytics add ('' 10, '1' 1, '' 0.1, '10^{-2}' 0.01, '' 0.001, '10^{-4}' 0.0001, '' 0.00001, '10^{-6}' 0.000001); \
           set mytics 10 ; \
           unset ylabel"
YTICS = " set ytics add ('' 10, '1' 1, '' 0.1, '10^{-2}' 0.01, '' 0.001, '10^{-4}' 0.0001, '' 0.00001, '10^{-6}' 0.000001); \
           set mytics 10 ; \
           set ylabel 'f_{signal}' offset 5.5,0"

NOKEY = "unset key"
KEY = "set key bottom right"

# Margins for each row resp. column
# ---- 0.95
# |  |
# ---- 0.70
# |  |
# ---- 0.45
# |  |
# ---- 0.20

TMARGIN = "set tmargin at screen 0.95; set bmargin at screen 0.70"
MMARGIN = "set tmargin at screen 0.70; set bmargin at screen 0.45"
BMARGIN = "set tmargin at screen 0.45; set bmargin at screen 0.20"
LMARGIN = "set lmargin at screen 0.18; set rmargin at screen 0.97"
#RMARGIN = "set lmargin at screen 0.55; set rmargin at screen 0.95"

# Placement of the a,b,c,d labels in the graphs
POS = "at graph 0.70, 0.77 font 'helvetica, 30'"
POS2 = "at graph 0.77, 0.25 font 'helvetica, 30'"

# Enable the use of macros
set macros

set output "RMSD_FSIG_SCATTER_PLOT.png"

XMIN = 0.000
XMAX = 0.59
YMIN = 0.0000002
YMAX = 0.0004
set yrange [YMIN : YMAX]
set xrange [XMIN : XMAX]

# Start multiplot
set multiplot layout 3,1 rowsfirst
# --- GRAPH a
@TMARGIN; @LMARGIN
@NOXTICS; @NOYTICS
@NOKEY
set label 1 '' @POS
#set logscale x 10
set logscale y 10
plot "f_rmsd_qmax4_20.dat" u 1:($2 / 1000) w p ls 1, \
     "f_rmsd_qmax8_20.dat" u 1:($2 / 1000) w p ls 7

# --- GRAPH b
@MMARGIN; @LMARGIN
@NOXTICS; @YTICS
@NOKEY
#set label 1 'N = 4,000' @POS
#plot "1restart_temp0_n4000_step0p01/CHI2_RMSD.dat" u 2:1 w p ls 8
plot "f_rmsd_qmax4_30.dat" u 1:($2 / 1000) w p ls 1, \
     "f_rmsd_qmax8_30.dat" u 1:($2 / 1000) w p ls 7

# --- GRAPH c
@BMARGIN; @LMARGIN
@XTICS; @NOYTICS
@NOKEY
#set label 1 'N = 20,000' @POS
#plot "1restart_temp0_n20000_step0p01/CHI2_RMSD.dat" u 2:1 w p ls 9
plot "f_rmsd_qmax4_40.dat" u 1:($2 / 1000) w p ls 1, \
     "f_rmsd_qmax8_40.dat" u 1:($2 / 1000) w p ls 7 , \
     #"f_rmsd_qmax4_50.dat" u 1:($2 / 1000) w p ls 1, \
     #"f_rmsd_qmax8_50.dat" u 1:($2 / 1000) w p ls 2

unset multiplot
### End multiplot

