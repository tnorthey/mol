reset

# png
set terminal pngcairo dashed size 2000,1600 enhanced font "Verdana,60"
#set terminal pngcairo dashed size 1000,800 enhanced font "Verdana,30"
#set terminal pngcairo dashed size 2500,1750 enhanced font "Verdana,50"
# dashed option enables dashed linestyle in pngcairo

# Custom line styles

LW1= 2.5
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

# STATS
stats "r05_dihedral_10_noise0_qmax25.dat" u 3 prefix "t10"
stats "r05_dihedral_20_noise0_qmax25.dat" u 3 prefix "t20"
stats "r05_dihedral_30_noise0_qmax25.dat" u 3 prefix "t30"
stats "r05_dihedral_35_noise0_qmax25.dat" u 3 prefix "t35"
stats "r05_dihedral_40_noise0_qmax25.dat" u 3 prefix "t40"
stats "r05_dihedral_50_noise0_qmax25.dat" u 3 prefix "t50"
stats "r05_dihedral_60_noise0_qmax25.dat" u 3 prefix "t60"
t10_range = t10_min + (t10_max - t10_min)/20
t20_range = t20_min + (t20_max - t20_min)/20
t30_range = t30_min + (t30_max - t30_min)/20
t35_range = t35_min + (t35_max - t35_min)/20
t40_range = t40_min + (t40_max - t40_min)/20
t50_range = t50_min + (t50_max - t50_min)/20
t60_range = t60_min + (t60_max - t60_min)/20

# MACROS
# x- and ytics for each row resp. column
NOXTICS = "set xtics ('' 0, '' 8, '' 16, '' 24); \
          unset xlabel; \
          set mxtics 2 "
XTICS = "set xtics 0, 0.5, 24; \
          set xlabel 'd_{05} (Å)' offset 0,0.4; \
          set mxtics 2"
NOYTICS = " set ytics add ('' 10, '1' 1, '' 0.1, '10^{-2}' 0.01, '' 0.001, '10^{-4}' 0.0001); \
           set mytics 2 ; \
           unset ylabel"
YTICS = "set ytics -200, 50, 200; \
           set mytics 2 ; \
           set ylabel 'ϕ_{0145} (°)' offset 1.5,0"

NOKEY = "unset key"
KEY = "set key bottom right font ',35'"

# Margins for each row resp. column
# ---- 0.95
# |  |
# ---- 0.70
# |  |
# ---- 0.45
# |  |
# ---- 0.20

TMARGIN = "set tmargin at screen 0.95; set bmargin at screen 0.20"
MMARGIN = "set tmargin at screen 0.60; set bmargin at screen 0.25"
BMARGIN = "set tmargin at screen 0.45; set bmargin at screen 0.20"
LMARGIN = "set lmargin at screen 0.18; set rmargin at screen 0.97"
#RMARGIN = "set lmargin at screen 0.55; set rmargin at screen 0.95"

# Placement of the a,b,c,d labels in the graphs
POS = "at graph 0.10, 0.86 font 'helvetica, 60'"
POS2 = "at graph 0.15, 0.32 font 'helvetica, 40'"
POS3 = "at graph 0.55, 0.45 font 'helvetica, 40'"

# Enable the use of macros
set macros

set output "PLOT_R05_DIHEDRAL_NOISE0_QMAX25_LOW50.png"

XMIN = 1.0
XMAX = 3.6
YMIN = -30
YMAX = 120
set yrange [YMIN : YMAX]
set xrange [XMIN : XMAX]

# Start multiplot
set multiplot layout 3,1 rowsfirst
# --- GRAPH a
@TMARGIN; @LMARGIN
@XTICS; @YTICS
@KEY
set label 1 'η = 0' @POS
#set label 1 '^↖ CHF_3' @POS
#set label 2 'CHD ^↗' @POS2
#set label 3 '_↙ Naphthalene' @POS3
#set logscale x 10
#set logscale y 10
LW = 4
LW2 = 1
DT1 = 1
DT2 = 2
DT3 = 3
array point1[1]
array point2[1]
array point3[1]
array point4[1]

# Plots the 100 with lowest energy (hard coded with values!)
plot "r05_dihedral_10_noise0_qmax25.dat" u 1:($3 < t10_range ? $2 : 1/0) t "10" w p pt 3 ps 2 lw 4 lc 6,\
     "r05_dihedral_20_noise0_qmax25.dat" u 1:($3 < t20_range ? $2 : 1/0) t "20" w p pt 6 ps 2 lw 4 lc 1,\
     "r05_dihedral_30_noise0_qmax25.dat" u 1:($3 < t30_range ? $2 : 1/0) t "30" w p pt 6 ps 2 lw 4 lc 2,\
     "r05_dihedral_35_noise0_qmax25.dat" u 1:($3 < t35_range ? $2 : 1/0) t "35" w p pt 6 ps 2 lw 4 lc 3,\
     "r05_dihedral_40_noise0_qmax25.dat" u 1:($3 < t40_range ? $2 : 1/0) t "40" w p pt 6 ps 2 lw 4 lc 4,\
     "r05_dihedral_50_noise0_qmax25.dat" u 1:($3 < t50_range ? $2 : 1/0) t "50" w p pt 6 ps 2 lw 4 lc 0,\
     "r05_dihedral_60_noise0_qmax25.dat" u 1:($3 < t60_range ? $2 : 1/0) t "60" w p pt 6 ps 2 lw 4 lc 6,\
     "target_r05_dihedral.dat" u 1:2 t "target" w lp pt 6 ps 3 lw 8 lc 7,\


#plot "r05_dihedral_10_noise0_qmax25.dat" u 1:($3 < -231.73190 ? $2 : 1/0) t "10" w p pt 3 ps 2 lw 4 lc 6,\
     #"r05_dihedral_20_noise0_qmax25.dat" u 1:($3 < -231.64213 ? $2 : 1/0) t "20" w p pt 6 ps 2 lw 4 lc 1,\
     #"r05_dihedral_30_noise0_qmax25.dat" u 1:($3 < -231.58000 ? $2 : 1/0) t "30" w p pt 6 ps 2 lw 4 lc 2,\
     #"r05_dihedral_35_noise0_qmax25.dat" u 1:($3 < -231.59450 ? $2 : 1/0) t "35" w p pt 6 ps 2 lw 4 lc 3,\
     #"r05_dihedral_40_noise0_qmax25.dat" u 1:($3 < -231.57030 ? $2 : 1/0) t "40" w p pt 6 ps 2 lw 4 lc 4,\
     #"r05_dihedral_50_noise0_qmax25.dat" u 1:($3 < -231.54275 ? $2 : 1/0) t "50" w p pt 6 ps 2 lw 4 lc 0,\
     #"r05_dihedral_60_noise0_qmax25.dat" u 1:($3 < -231.49180 ? $2 : 1/0) t "60" w p pt 6 ps 2 lw 4 lc 6,\
     #"target_r05_dihedral.dat" u 1:2 t "target" w lp pt 6 ps 3 lw 8 lc 7,\

unset multiplot
### End multiplot

