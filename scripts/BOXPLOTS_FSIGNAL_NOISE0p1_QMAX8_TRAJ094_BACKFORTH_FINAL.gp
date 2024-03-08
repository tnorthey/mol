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
stats "analysis_20_noise0p1_qmax8_traj094_backforth_Final.dat" u 3 prefix "t20"
stats "analysis_35_noise0p1_qmax8_traj094_backforth_Final.dat" u 3 prefix "t35"
stats "analysis_40_noise0p1_qmax8_traj094_backforth_Final.dat" u 3 prefix "t40"
stats "analysis_45_noise0p1_qmax8_traj094_backforth_Final.dat" u 3 prefix "t45"
stats "analysis_50_noise0p1_qmax8_traj094_backforth_Final.dat" u 3 prefix "t50"
stats "analysis_55_noise0p1_qmax8_traj094_backforth_Final.dat" u 3 prefix "t55"
stats "analysis_60_noise0p1_qmax8_traj094_backforth_Final.dat" u 3 prefix "t60"
stats "analysis_65_noise0p1_qmax8_traj094_backforth_Final.dat" u 3 prefix "t65"
stats "analysis_70_noise0p1_qmax8_traj094_backforth_Final.dat" u 3 prefix "t70"
stats "analysis_75_noise0p1_qmax8_traj094_backforth_Final.dat" u 3 prefix "t75"

t20_range = t20_median
t35_range = t35_median
t40_range = t40_median
t45_range = t45_median
t50_range = t50_median
t55_range = t55_median
t60_range = t60_median
t65_range = t65_median
t70_range = t70_median
t75_range = t75_median

# f_signal stats
stats "analysis_20_noise0p1_qmax8_traj094_backforth_Final.dat" u 4 prefix "f20"
stats "analysis_35_noise0p1_qmax8_traj094_backforth_Final.dat" u 4 prefix "f35"
stats "analysis_40_noise0p1_qmax8_traj094_backforth_Final.dat" u 4 prefix "f40"
stats "analysis_45_noise0p1_qmax8_traj094_backforth_Final.dat" u 4 prefix "f45"
stats "analysis_50_noise0p1_qmax8_traj094_backforth_Final.dat" u 4 prefix "f50"
stats "analysis_55_noise0p1_qmax8_traj094_backforth_Final.dat" u 4 prefix "f55"
stats "analysis_60_noise0p1_qmax8_traj094_backforth_Final.dat" u 4 prefix "f60"
stats "analysis_65_noise0p1_qmax8_traj094_backforth_Final.dat" u 4 prefix "f65"
stats "analysis_70_noise0p1_qmax8_traj094_backforth_Final.dat" u 4 prefix "f70"
stats "analysis_75_noise0p1_qmax8_traj094_backforth_Final.dat" u 4 prefix "f75"

# look at the range of fsignal values...
f20_range = f20_max 
f35_range = f35_max
f40_range = f40_max
f45_range = f45_max
f50_range = f50_max
f55_range = f55_max
f60_range = f60_max
f65_range = f65_max
f70_range = f70_max
f75_range = f75_max


# MACROS
# x- and ytics for each row resp. column
NOXTICS = "set xtics ('' 0, '' 8, '' 16, '' 24); \
          unset xlabel; \
          set mxtics 2 "
XTICS = "set xtics 0, 1.0, 24; \
          set xlabel 'time-step' offset 0,0.4; \
          set mxtics 2"
NOYTICS = " set ytics add ('' 10, '1' 1, '' 0.1, '10^{-2}' 0.01, '' 0.001, '10^{-4}' 0.0001); \
           set mytics 2 ; \
           unset ylabel"
YTICS = " set ytics add ('' 10, '1' 1, '' 0.1, '10^{-2}' 0.01, '' 0.001, '10^{-4}' 0.0001, '' 0.00001, '10^{-6}' 0.000001, '' 0.0000001); \
           set mytics 10 ; \
           set ylabel 'f_{signal}' offset 7.0,0"

NOKEY = "unset key"
KEY = "set key bottom right font ',35'"
KEY = "set key top left font ',35'"

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
POS = "at graph 0.22, 0.89 font 'helvetica, 60'"
POS2 = "at graph 0.15, 0.32 font 'helvetica, 40'"
POS3 = "at graph 0.55, 0.45 font 'helvetica, 40'"

# Enable the use of macros
set macros

set output "BOXPLOTS_FSIGNAL_NOISE0p1_QMAX8_TRAJ094_BACKFORTH_FINAL.png"

XMIN = 0.1
XMAX = 10.9
YMIN = 0.00000002
YMAX = 0.002
set yrange [YMIN : YMAX]
set xrange [XMIN : XMAX]

# Start multiplot
set multiplot layout 3,1 rowsfirst
# --- GRAPH a
@TMARGIN; @LMARGIN
@XTICS; @YTICS
@NOKEY
#set label 1 'η = 0' @POS
#set label 1 '^↖ CHF_3' @POS
#set label 2 'CHD ^↗' @POS2
#set label 3 '_↙ Naphthalene' @POS3
#set logscale x 10
set logscale y 10
LW = 4
LW2 = 1
DT1 = 1
DT2 = 2
DT3 = 3
array point1[1]
array point2[1]
array point3[1]
array point4[1]

#set style boxplot nooutliers
set style fill solid 0.5 border -1
set style boxplot outliers pointtype 7
set style data boxplot
set boxwidth  0.5
set pointsize 0.5
###By default the whiskers extend from the ends of the box to the most distant point whose y value lies within 1.5 times the interquartile range. By default outliers are drawn as circles (point type 7). The width of the bars at the end of the whiskers may be controlled using set bars or set errorbars. 

plot "analysis_20_noise0p1_qmax8_traj094_backforth_Final.dat" u (1.0):($3 < t20_range & $4 < f20_range ? $4 : 1/0) t "20",\
     "analysis_35_noise0p1_qmax8_traj094_backforth_Final.dat" u (2.0):($3 < t35_range & $4 < f35_range ? $4 : 1/0) t "35",\
     "analysis_40_noise0p1_qmax8_traj094_backforth_Final.dat" u (3.0):($3 < t40_range & $4 < f40_range ? $4 : 1/0) t "40",\
     "analysis_45_noise0p1_qmax8_traj094_backforth_Final.dat" u (4.0):($3 < t45_range & $4 < f45_range ? $4 : 1/0) t "45",\
     "analysis_50_noise0p1_qmax8_traj094_backforth_Final.dat" u (5.0):($3 < t50_range & $4 < f50_range ? $4 : 1/0) t "50",\
     "analysis_55_noise0p1_qmax8_traj094_backforth_Final.dat" u (6.0):($3 < t55_range & $4 < f55_range ? $4 : 1/0) t "55",\
     "analysis_60_noise0p1_qmax8_traj094_backforth_Final.dat" u (7.0):($3 < t60_range & $4 < f60_range ? $4 : 1/0) t "60",\
     "analysis_65_noise0p1_qmax8_traj094_backforth_Final.dat" u (8.0):($3 < t65_range & $4 < f65_range ? $4 : 1/0) t "65",\
     "analysis_70_noise0p1_qmax8_traj094_backforth_Final.dat" u (9.0):($3 < t70_range & $4 < f70_range ? $4 : 1/0) t "70",\
     "analysis_75_noise0p1_qmax8_traj094_backforth_Final.dat" u (10.0):($3 < t75_range & $4 < f75_range ? $4 : 1/0) t "75",\

unset multiplot
### End multiplot

