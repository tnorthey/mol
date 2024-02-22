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
stats "analysis_10_noise0_qmax8_traj094_test.dat" u 3 prefix "t10"
stats "analysis_20_noise0_qmax8_traj094_test.dat" u 3 prefix "t20"
stats "analysis_32_noise0_qmax8_traj094_test.dat" u 3 prefix "t32"
stats "analysis_35_noise0_qmax8_traj094_test.dat" u 3 prefix "t35"
#stats "analysis_37_noise0_qmax8_traj094_test.dat" u 3 prefix "t37"
#stats "analysis_40_noise0_qmax8_traj094_test.dat" u 3 prefix "t40"
#stats "analysis_44_noise0_qmax8_traj094_test.dat" u 3 prefix "t44"
#stats "analysis_50_noise0_qmax8_traj094_test.dat" u 3 prefix "t50"
#stats "analysis_55_noise0_qmax8_traj094_test.dat" u 3 prefix "t55"
#stats "analysis_60_noise0_qmax8_traj094_test.dat" u 3 prefix "t60"
#stats "analysis_65_noise0_qmax8_traj094_test.dat" u 3 prefix "t65"
#stats "analysis_70_noise0_qmax8_traj094_test.dat" u 3 prefix "t70"
#stats "analysis_75_noise0_qmax8_traj094_test.dat" u 3 prefix "t75"

t10_range = t10_up_quartile  # t10_median
t20_range = t20_up_quartile  # t20_median 
t32_range = t32_up_quartile  # t30_median 
t35_range = t35_up_quartile  # t30_median 
#t37_range = t37_up_quartile  # t30_median 
#t40_range = t40_up_quartile  # t40_median 
#t44_range = t44_up_quartile  # t40_median 
#t50_range = t50_up_quartile
#t55_range = t55_up_quartile
#t60_range = t60_up_quartile
#t65_range = t65_up_quartile
#t70_range = t70_up_quartile
#t75_range = t75_up_quartile

#t10_range = t10_up_quartile
#t20_range = t20_up_quartile
#t30_range = t30_up_quartile
#t40_range = t40_up_quartile
#t50_range = t50_up_quartile
#t60_range = t60_up_quartile
#t70_range = t70_up_quartile
#t75_range = t75_up_quartile

# MACROS
# x- and ytics for each row resp. column
NOXTICS = "set xtics ('' 0, '' 8, '' 16, '' 24); \
          unset xlabel; \
          set mxtics 2 "
XTICS = "set xtics 0, 1.5, 24; \
          set xlabel 'd_{05} (Å)' offset 0,0.4; \
          set mxtics 2"
NOYTICS = " set ytics add ('' 10, '1' 1, '' 0.1, '10^{-2}' 0.01, '' 0.001, '10^{-4}' 0.0001); \
           set mytics 2 ; \
           unset ylabel"
YTICS = "set ytics -200, 100, 400; \
           set mytics 2 ; \
           set ylabel 'ϕ_{0145} (°)' offset 1.5,0"

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
POS = "at graph 0.10, 0.46 font 'helvetica, 60'"
POS2 = "at graph 0.15, 0.32 font 'helvetica, 40'"
POS3 = "at graph 0.55, 0.45 font 'helvetica, 40'"

# Enable the use of macros
set macros

set output "PLOT_R05_DIHEDRAL_NOISE0_QMAX8_TRAJ094_TEST.png"

XMIN = 1.25
XMAX = 6.25
YMIN = 0
YMAX = 290
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
plot "analysis_10_noise0_qmax8_traj094_test.dat" u 1:($3 < t10_range ? $2 : 1/0) t "10" w p pt 3 ps 2 lw 1 lc 6,\
     "analysis_20_noise0_qmax8_traj094_test.dat" u 1:($3 < t20_range ? $2 : 1/0) t "20" w p pt 6 ps 2 lw 1 lc 5,\
     "analysis_32_noise0_qmax8_traj094_test.dat" u 1:($3 < t32_range ? $2 : 1/0) t "32" w p pt 1 ps 1 lw 1 lc 2,\
     "analysis_35_noise0_qmax8_traj094_test.dat" u 1:($3 < t35_range ? $2 : 1/0) t "35" w p pt 2 ps 1 lw 1 lc 2,\
     "analysis_37_noise0_qmax8_traj094_test.dat" u 1:($3 < t37_range ? $2 : 1/0) t "37" w p pt 3 ps 1 lw 1 lc 2,\
     "analysis_40_noise0_qmax8_traj094_test.dat" u 1:($3 < t40_range ? $2 : 1/0) t "40" w p pt 6 ps 2 lw 1 lc 4,\
     "analysis_44_noise0_qmax8_traj094_test.dat" u 1:($3 < t44_range ? $2 : 1/0) t "44" w p pt 3 ps 2 lw 1 lc 4,\
     "analysis_50_noise0_qmax8_traj094_test.dat" u 1:($3 < t50_range ? $2 : 1/0) t "50" w p pt 1 ps 2 lw 1 lc 6,\
     "analysis_55_noise0_qmax8_traj094_test.dat" u 1:($3 < t55_range ? $2 : 1/0) t "55" w p pt 2 ps 2 lw 1 lc 6,\
     "analysis_60_noise0_qmax8_traj094_test.dat" u 1:($3 < t60_range ? $2 : 1/0) t "60" w p pt 6 ps 2 lw 4 lc 6,\
     "analysis_65_noise0_qmax8_traj094_test.dat" u 1:($3 < t65_range ? $2 : 1/0) t "65" w p pt 2 ps 2 lw 4 lc 6,\
     "analysis_70_noise0_qmax8_traj094_test.dat" u 1:($3 < t70_range ? $2 : 1/0) t "70" w p pt 6 ps 2 lw 4 lc 0,\
     "analysis_75_noise0_qmax8_traj094_test.dat" u 1:($3 < t75_range ? $2 : 1/0) t "75" w p pt 5 ps 1 lw 1 lc 3,\
     "target_r05_dihedral_traj094_points_tdouble.dat" u 1:2 t "target" w p pt 6 ps 3 lw 8 lc 7,\
     "target_r05_dihedral_traj094.dat" u 1:2 t "" w l lw 4 lc 7,\


#plot "analysis_10_noise0_qmax8.dat" u 1:($3 < -231.73190 ? $2 : 1/0) t "10" w p pt 3 ps 2 lw 4 lc 6,\
     #"analysis_20_noise0_qmax8.dat" u 1:($3 < -231.64213 ? $2 : 1/0) t "20" w p pt 6 ps 2 lw 4 lc 1,\
     #"analysis_30_noise0_qmax8.dat" u 1:($3 < -231.58000 ? $2 : 1/0) t "30" w p pt 6 ps 2 lw 4 lc 2,\
     #"analysis_35_noise0_qmax8.dat" u 1:($3 < -231.59450 ? $2 : 1/0) t "35" w p pt 6 ps 2 lw 4 lc 3,\
     #"analysis_40_noise0_qmax8.dat" u 1:($3 < -231.57030 ? $2 : 1/0) t "40" w p pt 6 ps 2 lw 4 lc 4,\
     #"analysis_50_noise0_qmax8.dat" u 1:($3 < -231.54275 ? $2 : 1/0) t "50" w p pt 6 ps 2 lw 4 lc 0,\
     #"analysis_60_noise0_qmax8.dat" u 1:($3 < -231.49180 ? $2 : 1/0) t "60" w p pt 6 ps 2 lw 4 lc 6,\
     #"target_r05_dihedral.dat" u 1:2 t "target" w lp pt 6 ps 3 lw 8 lc 7,\

unset multiplot
### End multiplot

