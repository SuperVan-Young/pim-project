.title A MOSTEST DC RUN  IDS=f(VDS，VGS)
.options list node post
*
.protect
.INCLUDE '45nm_HP.pm'
.unprotect
.options post=2 list

*Source
VDS NodeD 0 DC 5V
VGS NodeG 0 DC 5V

*Circuit
MN0 NodeD NodeG 0 0 NMOS L=2u W=10u

*Simulation
.DC  VDS 0 5 0.001 VGS 0 5 0.5
.PRINT V(NodeD) V(NodeG) I(MN0)
.PLOT V(NodeD) V(NodeG)  I(MN0)
*
.END

