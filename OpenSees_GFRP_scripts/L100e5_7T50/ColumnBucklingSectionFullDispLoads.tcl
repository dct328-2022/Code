set timelist "0.0 5.0 10.0 15.0 20.0 25.0 30.0 35.0 40.0 45.0 50.0 55.0"
set loadlist "0.0 -4449.46289063 -5657.95898 -6976.31835938 -8660.88867188 -10473.6328125 -12579.34570313 -14355.46875 -14703.36914063 -16497.80273438 -16754.15039063 -17266.84570313"
set M1 "0.0 14210.668148810975 18202.133585670043 22264.437067567873 27178.687594172065 32973.91738328835 37770.11632307874 39265.756890243836 41810.057256625325 43385.396538174144 46112.978629726764 49861.98645507402"
set M2 "0.0 -6963.544715115358 -8200.374743237255 -9707.680507754405 -13124.654426583154 -14247.312374952628 -16374.29344832397 -18948.22811013565 -17842.877594277197 -20201.359171546745 -18917.426516278734 -15341.026762143727"
set timetotal 55

set vl 99.23579

model basic -ndm 2 -ndf 3

node 1 0 0

set width 40.0
set thickness 9.5
set mat_thickness 0.717
set fc 94.72
set fs 11.1
set E 16383
#set E 18519.5

set div 20

geomTransf Corotational 1

set MCfactor 1

# Average D values
set D1 0.000596184
set D2 0.001202012
set D3 0.001864756
set D4 0.002389663
set D5 0.003390781
set D6 0.003701686
set D7 0.004

# highest D values
#set D1 0.000730701
#set D2 0.001472459
#set D3 0.002280459
#set D4 0.002932505
#set D5 0.00414572
#set D6 0.004517152
#set D7 0.005

set D1 [expr $D1 * $MCfactor]
set D2 [expr $D2 * $MCfactor]
set D3 [expr $D3 * $MCfactor]
set D4 [expr $D4 * $MCfactor]
set D5 [expr $D5 * $MCfactor]
set D6 [expr $D6 * $MCfactor]
set D7 [expr $D7 * $MCfactor]

# Moment-curvature relationship (40 mm width)
uniaxialMaterial ElasticMultiLinear 1 -strain [expr -$D7] [expr -$D6] [expr -$D5] [expr -$D4] [expr -$D3] [expr -$D2] [expr -$D1] 0 [expr $D1] [expr $D2] [expr $D3] [expr $D4] [expr $D5] [expr $D6] [expr $D7] -stress -100000 -110722.5 -108176.5 -90506.5 -69093.5 -47376.5 -23930.5 0 23930.5 47376.5 69093.5 90506.5 108176.5 110722.5 100000

# Shear force-shear strain relationship (40 mm x 9.5 mm)
uniaxialMaterial ElasticMultiLinear 2 -strain -0.08 -0.074124631 -0.063475462 -0.053212344 -0.043137707 -0.033336626 -0.023958493 -0.015216825 -0.007202479 0 0.007202479 0.015216825 0.023958493 0.033336626 0.043137707 0.053212344 0.063475462 0.074124631 0.08 -stress -2705.80014 -2805.103484 -2761.620896 -2641.208955 -2481.315423 -2261.317412 -1939.430846 -1470.828856 -830.5999999 0 830.5999999 1470.828856 1939.430846 2261.317412 2481.315423 2641.208955 2761.620896 2805.103484 2705.80014

# Normal stress-strain relationship for roving (standard)
uniaxialMaterial ElasticMultiLinear 3 -strain -0.05 -0.0107522 -0.01 -0.008 -0.006 -0.004 0 0.004 0.006 0.008 0.01 0.0107522 0.05 -stress -237.5 -237.490477380061 -228.507922578270 -195.655534483196 -143.838458892024 -96.3838428498649 0 96.3838428498649 143.838458892024 195.655534483196 228.507922578270 237.490477380061 237.5

# Normal stress-strain relationship for roving
#uniaxialMaterial ElasticMultiLinear 3 -strain -0.05 -0.0107522 -0.01 -0.008 -0.006 -0.004 0 0.004 0.006 0.008 0.01 0.0107522 0.05 -stress -230.1 -236 -228.507922578270 -195.655534483196 -143.838458892024 -96.3838428498649 0 96.3838428498649 143.838458892024 195.655534483196 228.507922578270 230 230.1

# Normal stress-strain relationship for mat (standard)
uniaxialMaterial ElasticMultiLinear 4 -strain -0.0107522 -0.01 -0.008 -0.006 -0.004 -0.002 0 0.002 0.004 0.006 0.008 0.01 0.0107522 -stress -18.3372310943586 -18.3370327301791 -10.1761613871789 -10.1761613871789 -10.1761613871787 -10.1761613871787 0 10.1761613871787 10.1761613871787 10.1761613871789 10.1761613871789 18.3370327301791 18.3372310943586

# Tensile force - tensile strain relationship
uniaxialMaterial Elastic 5 [expr {$E*$width*$thickness}]

# Rigid shear
uniaxialMaterial Elastic 6 11532141

# Fibre section base
set rov_thickness [expr ($thickness-5*$mat_thickness)/4]
section Fiber 10 {
patch rect 4 10 10 [expr -$thickness/2] [expr -$width/2] [expr -$thickness/2+$mat_thickness] [expr $width/2]
patch rect 3 20 10 [expr -$thickness/2+$mat_thickness] [expr -$width/2] [expr -$thickness/2+$mat_thickness+$rov_thickness] [expr $width/2]
patch rect 4 10 10 [expr -$thickness/2+$mat_thickness+$rov_thickness] [expr -$width/2] [expr -$thickness/2+2*$mat_thickness+$rov_thickness] [expr $width/2]
patch rect 3 20 10 [expr -$thickness/2+2*$mat_thickness+$rov_thickness] [expr -$width/2] [expr -$thickness/2+2*$mat_thickness+2*$rov_thickness] [expr $width/2]
patch rect 4 10 10 [expr -$thickness/2+2*$mat_thickness+2*$rov_thickness] [expr -$width/2] [expr -$thickness/2+3*$mat_thickness+2*$rov_thickness] [expr $width/2]
patch rect 3 20 10 [expr -$thickness/2+3*$mat_thickness+2*$rov_thickness] [expr -$width/2] [expr -$thickness/2+3*$mat_thickness+3*$rov_thickness] [expr $width/2]
patch rect 4 10 10 [expr -$thickness/2+3*$mat_thickness+3*$rov_thickness] [expr -$width/2] [expr -$thickness/2+4*$mat_thickness+3*$rov_thickness] [expr $width/2]
patch rect 3 20 10 [expr -$thickness/2+4*$mat_thickness+3*$rov_thickness] [expr -$width/2] [expr -$thickness/2+4*$mat_thickness+4*$rov_thickness] [expr $width/2]
patch rect 4 10 10 [expr -$thickness/2+4*$mat_thickness+4*$rov_thickness] [expr -$width/2] [expr -$thickness/2+5*$mat_thickness+4*$rov_thickness] [expr $width/2]
}

#section Aggregator 1 2 Vy -section 10
section Aggregator 1 2 Vy 1 Mz 5 P
#section Aggregator 1 6 Vy 1 Mz 5 P

set increvli [expr {$vl/$div}]
set vli $increvli
set Area [expr $width * $thickness]
set MI [expr $width * $thickness * $thickness * $thickness/12]
set EulerLoad [expr 3.1415926*3.1415926*$E*$MI/$vl/$vl]
set MaxLoad [expr floor(-1.05*$EulerLoad)]

set i 2

for {set vli $increvli} {$vli < [expr $vl + 1]} {set vli [expr $vli + $increvli]} {
node $i 0 $vli -mass 0.00001 0.00001 0.00001
element forceBeamColumn [expr $i - 1] [expr $i - 1] $i 10 1 1 -integration Legendre -iter 300 1e-15
set i [expr $i + 1]
}


fix 1 1 1 0
fix [expr {$div + 1}] 1 0 0

recorder Node -file MidDisplacement.out -time -node [expr $div/2+1] -dof 1 disp
recorder Node -file TopDisplacement.out -time -node [expr $div+1] -dof 2 disp
recorder Node -file BottomReaction.out -time -node 1 -dof 1 2 3 reaction
recorder Node -file TopReaction.out -time -node [expr $div+1] -dof 1 2 3 reaction
recorder Node -file NodeRotation.out -time -node 1 [expr {$div + 1}] -dof 3 disp
recorder Node -file NodeHorizontalDisp.out -time -nodeRange 1 [expr {$div + 1}] -dof 1 disp

#recorder Element -file ElementLocalForces.out -time -eleRange 1 [expr $div] localForce
#recorder Element -file MidElementDeformation.out -time -ele [expr $div/2] section 10 deformation

timeSeries Path 11 -time $timelist -values $loadlist
timeSeries Path 12 -time $timelist -values $M1
timeSeries Path 13 -time $timelist -values $M2

pattern Plain 2 11 {
load [expr {$div + 1}] 0 1 0
}

pattern Plain 3 13 {
load [expr {$div + 1}] 0 0 1
}

pattern Plain 4 12 {
load 1 0 0 1
}

constraints Transformation     				# how it handles boundary conditions
numberer RCM					# renumber dof's to minimize band-width (optimization), if you want to
system SparseSPD				# how to store and solve the system of equations in the analysis
test EnergyIncr 1.0e-8 400 2 2
algorithm KrylovNewton
#algorithm BFGS
integrator  LoadControl 1 $timetotal
analysis Static					# define type of analysis static or transient
analyze $timetotal
wipe