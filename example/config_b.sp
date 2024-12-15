* 8 SRAM cells - Static I-V Curve Simulation for Read Port
.options list node post
*
.protect
.INCLUDE '45nm_HP.pm'
.unprotect
.options post=2 list

*Source
VQ Q 0 DC 0.65
Vin WL 0 DC 0.0
Vbias SL 0 DC 0.65

*Circuit
M1 SL Q N 0 NMOS L=45n W=90n
M2 N WL BL 0 NMOS L=45n W=90n
RBL BL 0 50

*Simulation
.DC Vin 0 0.65 0.01
.PRINT V(WL) I(RBL)
.PLOT  V(WL) I(RBL)

.PROBE I(RBL)
.END