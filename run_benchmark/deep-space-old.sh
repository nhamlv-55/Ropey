#!/usr/bin/env bash

CPU=930
MEM=16384

# 0 -- original iuc code
IUC=1
# only active when IUC>0
IUC_ARITH=1
IUC_OLD_HYPREDUCE=false
IUC_FARKAS_STATS=false
MBP=true
ELIM_AUX=true

PROJECT=/ag/chc-comp18
time $PROJECT/bin/z3-deep-space-static -st -v:1 fixedpoint.xform.slice=true fixedpoint.xform.inline_linear=true fixedpoint.xform.inline_eager=true fixedpoint.xform.tail_simplifier_pve=false fixedpoint.engine=spacer fixedpoint.print_statistics=true fixedpoint.spacer.elim_aux=$ELIM_AUX fixedpoint.spacer.reach_dnf=true fixedpoint.spacer.iuc=$IUC fixedpoint.spacer.iuc.arith=$IUC_ARITH fixedpoint.pdr.validate_result=false  fixedpoint.spacer.ground_cti=true fixedpoint.spacer.mbqi=false fixedpoint.spacer.iuc.print_farkas_stats=$IUC_FARKAS_STATS fixedpoint.spacer.iuc.old_hyp_reducer=$IUC_OLD_HYPREDUCE fixedpoint.spacer.ctp=true fixedpoint.spacer.native_mbp=$MBP -T:$CPU -memory:$MEM $1 

