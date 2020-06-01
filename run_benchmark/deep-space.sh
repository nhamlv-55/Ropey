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
time $PROJECT/bin/z3-deep-space-static -st -v:1 fp.xform.slice=true fp.xform.inline_linear=true fp.xform.inline_eager=true fp.xform.tail_simplifier_pve=false fp.engine=spacer fp.print_statistics=true fp.spacer.elim_aux=$ELIM_AUX fp.spacer.reach_dnf=true fp.spacer.iuc=$IUC fp.spacer.iuc.arith=$IUC_ARITH fp.validate=true fp.spacer.ground_pobs=true fp.spacer.mbqi=false fp.spacer.iuc.print_farkas_stats=$IUC_FARKAS_STATS fp.spacer.iuc.old_hyp_reducer=$IUC_OLD_HYPREDUCE fp.spacer.ctp=true fp.spacer.native_mbp=$MBP -T:$CPU -memory:$MEM $1 

