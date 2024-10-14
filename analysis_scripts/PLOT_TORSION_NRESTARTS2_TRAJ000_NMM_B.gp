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
array trange[54]
do for [i=18:54] {
    filename = sprintf("analysis_%02d_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat", i)
    stats filename u 6 prefix sprintf("t%02d", i)
}
trange[18] = t18_lo_quartile  # t20_median 
trange[19] = t19_lo_quartile  # t20_median 
trange[20] = t20_lo_quartile  # t30_median 
trange[21] = t21_lo_quartile  # t30_median 
trange[22] = t22_lo_quartile  # t30_median 
trange[23] = t23_lo_quartile  # t40_median 
trange[24] = t24_lo_quartile  # t40_median 
trange[25] = t25_lo_quartile
trange[26] = t26_lo_quartile
trange[27] = t27_lo_quartile
trange[28] = t28_lo_quartile
trange[29] = t29_lo_quartile
trange[30] = t30_lo_quartile
trange[31] = t31_lo_quartile
trange[32] = t32_lo_quartile
trange[33] = t33_lo_quartile
trange[34] = t34_lo_quartile
trange[35] = t35_lo_quartile
trange[36] = t36_lo_quartile
trange[37] = t37_lo_quartile
trange[38] = t38_lo_quartile
trange[39] = t39_lo_quartile
trange[40] = t40_lo_quartile
trange[41] = t41_lo_quartile
trange[42] = t42_lo_quartile
trange[43] = t43_lo_quartile
trange[44] = t44_lo_quartile
trange[45] = t45_lo_quartile
trange[46] = t46_lo_quartile
trange[47] = t47_lo_quartile
trange[48] = t48_lo_quartile
trange[49] = t49_lo_quartile
trange[50] = t50_lo_quartile
trange[51] = t51_lo_quartile
trange[52] = t52_lo_quartile
trange[53] = t53_lo_quartile
trange[54] = t54_lo_quartile

# f_signal stats
array frange[54]
do for [i=18:54] {
    filename = sprintf("analysis_%02d_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat", i)
    stats filename u 4 prefix sprintf("f%02d", i)
}
frange[18] = f18_max+1  # t20_median 
frange[19] = f19_max+1  # t20_median 
frange[20] = f20_max+1  # t30_median 
frange[21] = f21_max+1  # t30_median 
frange[22] = f22_max+1  # t30_median 
frange[23] = f23_max+1  # t40_median 
frange[24] = f24_max+1  # t40_median 
frange[25] = f25_max+1
frange[26] = f26_max+1
frange[27] = f27_max+1
frange[28] = f28_max+1
frange[29] = f29_max+1
frange[30] = f30_max+1
frange[31] = f31_max+1
frange[32] = f32_max+1
frange[33] = f33_max+1
frange[34] = f34_max+1
frange[35] = f35_max+1
frange[36] = f36_max+1
frange[37] = f37_max+1
frange[38] = f38_max+1
frange[39] = f39_max+1
frange[40] = f40_max+1
frange[41] = f41_max+1
frange[42] = f42_max+1
frange[43] = f43_max+1
frange[44] = f44_max+1
frange[45] = f45_max+1
frange[46] = f46_max+1
frange[47] = f47_max+1
frange[48] = f48_max+1
frange[49] = f49_max+1
frange[50] = f50_max+1
frange[51] = f51_max+1
frange[52] = f52_max+1
frange[53] = f53_max+1
frange[54] = f54_max+1

print trange
print frange

# MACROS
# x- and ytics for each row resp. column
NOXTICS = "set xtics ('' 0, '' 8, '' 16, '' 24); \
          unset xlabel; \
          set mxtics 2 "
XTICS = "set xtics 0, 4, 20;\
         set xtics add ('' 0, '0' 2, '' 4, '0.2' 6, '' 8, '0.4' 10, '' 12, '0.6' 14, '' 16, '0.8' 18); \
         set mxtics 2; \
         set xlabel 't (ps)' offset 0,0.4"
NOYTICS = " set ytics add ('' 10, '1' 1, '' 0.1, '10^{-2}' 0.01, '' 0.001, '10^{-4}' 0.0001); \
           set mytics 2 ; \
           unset ylabel"
YTICS = "set ytics -100, 20, 100; \
           set mytics 2 ; \
           set ylabel 'ϕ_{C-N-C-C} (°)' offset 1.5,0"

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

set output "PLOT_TORSION_NRESTARTS2_TRAJ000_NMM_B.png"

XMIN = -0.5
XMAX = 36.5
YMIN = -65
YMAX = 115
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

do for [i=18:54] {
    filename = sprintf("analysis_%02d_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat", i)
    p filename u (i-18):($6 < trange[i] & $4 < frange[i] ? $3 : 1/0) t "18" w p pt 6 ps 2 lw 3 lc 8
}
p "nmm_geommovie_dihedral_6_3_10_5_modified.dat" u 1:($2 + 180) t "" w p pt 6 ps 4 lw 8 lc 7

unset multiplot
### End multiplot

