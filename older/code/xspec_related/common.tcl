# useful xspec routines
# Jeremy Sanders
# please acknowledge the use of these routines

set pct_version "1.0.50 (2008-10-29)"

puts "Loading JSS common routines ${pct_version} (Jeremy Sanders 2003-2008)"

# Changelog:
#  1.0.4: Fix no of datagroups in pct_list_chi2
#  1.0.5: Support adding lists of parameters to many commands
#  1.0.6: Add pct_tie
#  1.0.7: Modify pct_profile_error and pct_profile so you don't
#         have to specify parameters in a list (modified ordering too!!)
#  1.0.8: Allow paramters not to be in the first datagroup
#  1.0.9: Hidden some internal routines (with underscore)
#  1.0.10: Print out "read terr" for pct_profile_error
#  1.0.11: Print out flags on errors for pct_profile_error (+ minor cleanup)
#  1.0.12: Add pct_construct_[1t,2t]_apec, pct_construct_1t_vapec
#  1.0.13: Allow ranges of parameters
#  1.0.14: Allow multiple ranges in pct_rellink + (minor cleanup)
#  1.0.15: Add pct_construct_2t_vapec + add pct_fit_params variable +
#          save a backup file when making a profile as progressing
#  1.0.16: Add pct_plot_vff
#  1.0.17: Add pct_construct_2t_vmekal + minor cleanups
#  1.0.18: Modified output of pct_profile_error and pct_profile to use
#          skip single
#  1.0.19: Added pct_construct_mkcflow, added warnings for construct commands
#  1.0.20: Added pct_construct_1t_vmekal & pct_construct_1t_vmekal_gaussian
#          pct_construct_mulgas
#  1.0.21: Added pct_profile_error_channel & pct_profile_channel
#  1.0.22: Clever pct_profile_error ordering of parameters
#          (if finds new minimum, continues at that parameter)
#  1.0.23: Add fixnorm
#  1.0.24: Add pct_untie_in_dg, pct_thaw_in_dg & pct_freeze_in_dg 
#  1.0.25: pct_plot_density_channel, pct_plot_tcool_channel
#  1.0.26: Modify radius getting to use "tclout xflt"
#  1.0.27: Added pct_construct_mekal_powerlaw
#  1.0.28: Added pct_plot_pressure_channel
#  1.0.29: Fixed support from xspec 11.3.1
#  1.0.30: Fixed cooling time calcn
#  1.0.31: Added gas mass & gas mass per cooling time
#  1.0.32: Automatically calculate angular diameter distances
#  1.0.33: Added pct_plot_phys_errors
#  1.0.34: Fixed keyword getting
#  1.0.35: Use backup file dependent on hostname and pid
#  1.0.36: Change cosmology distance functions to be public
#  1.0.37: Change tclout parameter to tclout param
#  1.0.38: Add entropy calculation in pct_plot_phys_errors
#  1.0.39: Fixes for xspec12 (in _pct_find_error)
#  1.0.40: Further xspec12 fixes
#  1.0.41: Fix radii for multiple datagroups, format radius with %e for align
#  1.0.42: fixno_construct_multitemp_rm minor changes
#  1.0.43: add construct_multitemp
#  1.0.44: add _pct_free_params
#  1.0.45: add pct_construct_apec_powerlaw
#  1.0.46: add construct_multitemp_vapec_gsmooth & construct_multitemp_vapec
#  1.0.47: add cooling_time
#  1.0.48: some formatting fixes
#  1.0.49: add random number seeder
#  1.0.50: add pct_use_chain option to use chain to get best fitting val

# file prefix and and suffix
set pct_prefix xaf_
set pct_suffix _grp_spec.fits
set pct_fit_params "100 1e-2"


# default energy ranges to read data in
set pct_ignore_start 0.5
set pct_ignore_end 7.0

set pct_H0 70.
set pct_lambda 0.7

# set this to 1 to use the median value from the chain rather
# than the best fitting values when calculating error bars
set pct_use_chain 0

# get header key from fits file
proc _pct_get_header_key {file key} {
    # uses FTOOL FKEYPRINT program
    set retn [exec fkeyprint "$file" "$key" exact=yes]

    # matches KEY=VAL (with optional spaces)
    set rkey ""
    set rval ""
    set match ""
    regexp  -line {^([[:alnum:]]+?)[ ]*=[ ]*?([0-9A-Za-z\.Ee+-]+).*?$} $retn match rkey rval

    # simple check to see whether things went okay
    if { $rkey != $key } {
	puts "** Error getting key from $file"
    }

    return $rval
}

# get number of datagroups
proc _pct_get_no_dg {} {
    tclout datagrp
    return [expr {$xspec_tclout*1}]
}

# get parameter with model name and param name
# eg _pct_get_param_named projct major
proc _pct_get_param_named { cmptname paramname } {
    set nocmpts [_pct_tclout modcomp]

    # find component
    for { set c 1 } {$c <= $nocmpts} {incr c} {
	set cinfo [_pct_tclout compinfo $c]
	set name [lindex $cinfo 0]
	if { $name == $cmptname } {
	    break
	}
    }

    if { $name != $cmptname } {
	puts "ERROR: could not find component $cmptname"
	return ""
    }

    set baseparam [lindex $cinfo 1]
    set noparams [lindex $cinfo 2]

    for { set p $baseparam } {$p < ($baseparam+$noparams)} {incr p} {
	set name [lindex [_pct_tclout pinfo $p] 0]

	if { $name == $paramname } {
	    break
	}
    }

    if { $name != $paramname } {
	puts "ERROR: could not find parameter $paramname"
	return ""
    }

    return $p
}

proc _get_params_named { cmptname paramname } {
    set numpars [_pct_tclout modpar]
    set numcmpts [_pct_tclout modcomp]

    set thiscmpt 1
    set thiscmptname [lindex [_pct_tclout compinfo $thiscmpt] 0]
    set numcmptpars [lindex [_pct_tclout compinfo $thiscmpt] 2]
    set thiscmptct 0

    set out {}

    for { set p 1 } { $p <= $numpars } {incr p} {

	set thisparamname [lindex [_pct_tclout pinfo $p] 0]

	if { ($thisparamname == $paramname) && ($thiscmptname == $cmptname) } {
	    lappend out $p
	}

	incr thiscmptct
	if { $thiscmptct == $numcmptpars } {
	    incr thiscmpt
	    if { $thiscmpt <= $numcmpts} {
		set thiscmptname [lindex [_pct_tclout compinfo $thiscmpt] 0]
		set numcmptpars [lindex [_pct_tclout compinfo $thiscmpt] 2]
		set thiscmptct 0
	    }
	}

    }

    return $out
}

# get number of parameters per datagroup
proc _pct_get_params_per_dg {} {
    set no_datagrp [_pct_get_no_dg]
    tclout modpar
    set no_params $xspec_tclout
    set multiplier [expr {$no_params/$no_datagrp}]

    return $multiplier
}

# get number of parameter from datagroup and offset
#  (automatically adjusting offset if it isn't in the first group)
proc _pct_offset { dg offset } {
    set mult [_pct_get_params_per_dg]

    # renormalise offset
    while { $offset > $mult } { incr offset [expr {$mult * -1} ] }

    return [expr {$dg*$mult + $offset}]
}

# return the value of the xspec parameter at offset in datagroup dg
proc _pct_get_param { dg offset } {
    tclout param [_pct_offset $dg $offset]
    return [lindex $xspec_tclout 0]
}

# tclout as a function (to avoid extra lines)
proc _pct_tclout { args } {
    eval tclout $args
    return $xspec_tclout
}

# internal routine to expand out ranges of numbers
# works on the variable directly
proc _pct_expand_args { theargs } {
    upvar $theargs up_args

    set out_args {}
    # go through each arg and expand if there's a range specified
    foreach arg $up_args {
	if {[ string match ?*-?* $arg ]} {
	    # convert - to space
	    set arg [string map {- " "} $arg]
	    set first [lindex $arg 0]
	    set last [lindex $arg 1]
	    for { set i $first } { $i <= $last} { incr i } {
		lappend out_args $i
	    }
	    continue
	}

	# check not alphabetical

	
	# normal argument
	lappend out_args $arg
    }

    set up_args $out_args
}

# get list of free parameters in model
proc _pct_free_params {} {
    set num [_pct_tclout modpar]
    set retn ""
    for {set p 1} {$p <= $num} {incr p} {
	set delta [lindex [_pct_tclout param $p] 1]
	set linked [lindex [_pct_tclout plink $p] 0]

	if { $delta > 0. && $linked == "F" } {
	    lappend retn $p
	}
    }
    return $retn
}

# load datasets start_no:end_no
proc pct_load_data { first_no inner_radius start_no end_no } {
    global pct_prefix pct_suffix
    global pct_ignore_start pct_ignore_end

    data none

    set count 1
    for { set i $start_no } { $i <= $end_no } {incr i} {
	data $count:$count ${pct_prefix}${i}${pct_suffix}
	incr count
    }
    ignore **:**-${pct_ignore_start}
    ignore **:${pct_ignore_end}-**
    ignore bad **

    if { $start_no == $first_no } {
	set radius $inner_radius
    } else {
	set filename  ${pct_prefix}[expr {$start_no-1}]${pct_suffix}
	set radius [_pct_get_header_key $filename XFLT0001]
    }

    #if { [ _pct_tclout modpar ] > 2 } {
#	newpar 1 "$radius -1 0 0 $radius $radius"
#	newpar 2 "$radius -1 0 0 $radius $radius"
#    }
    return
}

# return list containing radii and errors for each datagroup
proc _pct_get_radii {} {
    # get inner major axis
    tclout param [_pct_get_param_named projct major]

    set prev_radius [lindex $xspec_tclout 0]
    set no_datagrp [_pct_get_no_dg]
    tclout datasets
    set no_dataset $xspec_tclout

    # datasets per datagrp
    set dsperdg [expr {$no_dataset/$no_datagrp}]

    set retn {}
    for { set dg 1 } { $dg <= $no_datagrp } {incr dg} {
	tclout xflt [expr {($dg-1)*$dsperdg +1}]
	set outer_radius [lindex $xspec_tclout 1]
	#tclout filename $dg
	#set outer_radius [_pct_get_header_key $xspec_tclout XFLT0001]
	set radius [expr {($prev_radius+$outer_radius)*0.5}]
	set radius_err [expr {($outer_radius-$prev_radius)*0.5}]

	lappend retn [format "%.4e %.4e" $radius $radius_err]
	set prev_radius $outer_radius
    }

    return $retn
}

# calculate a profile for a projct model
proc pct_profile { args } {
    eval pct_profile_channel stdout $args
}

# calculate a profile for the parameters, and output to a channel
proc pct_profile_channel { chan args } {
    _pct_expand_args args
    set no_datagrp [_pct_get_no_dg]

    # qdp header
    puts $chan "skip single"
    puts $chan "read serr 1"
    set radii [_pct_get_radii]

    # print parameters
    foreach param $args {
	tclout pinfo $param
	puts $chan "! Parameter $param (${xspec_tclout})"
	for { set dg 0 } { $dg < $no_datagrp } {incr dg} {
	    tclout param [_pct_offset $dg $param]
	    puts $chan "[lindex $radii $dg] [lindex $xspec_tclout 0]"
	}
	puts $chan "no no no"
    }
}

# get error on a particular parameter, return XX if new minimum
proc _pct_find_error { param delchi2 } {
    global pct_use_chain

    if { ${pct_use_chain} } {
	# get median using error command
	error maximum 2000 0.001 $param
	tclout error $param
	set val [expr 0.5*([lindex $xspec_tclout 0]+[lindex $xspec_tclout 1])]
    } else {
	# use best fitting parameter
	tclout param $param
	scan "$xspec_tclout" {%f} val
    }
    
    error maximum 2000 [expr {$delchi2*1.0}] $param
    tclout error $param
    scan "$xspec_tclout" {%f %f %s} minerr maxerr flags
    
    # return values (in +/- form) and status code
    set retn [format "%.4e %.4e %.4e %s" $val [expr $maxerr-$val] [expr $minerr-$val] $flags]

    return $retn
}

# return a list containing the errors and flags for the list of
# parameters in params, repeating fits if necessary (i.e. new
# minima found).
proc _pct_get_error_list { params delchi2 } {
    global pct_fit_params
    global pct_use_chain

    set backup_file pct_backup_[pid]_[info hostname].xcm

    # list contains order in which to get errors of parameters
    set params_copy $params
    set noparams [llength $params]

    while {1} {
	# back up in case we want to stop
	file delete $backup_file
	save all $backup_file

	query no
	if { ! ${pct_use_chain} } { 
	    eval fit ${pct_fit_params}
	}

	# back up again
	file delete $backup_file
	save all $backup_file

	set errorlist { }
	set newmin 0

	# iterate over error_order (dereference to get param no)
	for {set i 0} {$i < $noparams} {incr i} {
	    set p [lindex $params_copy $i]
	    tclout pinfo $p
	    puts "@@@ Finding error for parameter $p (${xspec_tclout})"
	    set error [_pct_find_error $p $delchi2]

	    # repeat outer loop if there's a new minimum
	    set flags [lindex $error 3]
	    if { [string index $flags 0] == "T" } {
		set newmin 1
		puts "@@@ Looping as new minimum found"

		# make this parameter first next time around
		set l1 [lrange $params_copy 0 [expr $i-1]]
		set l2 [lrange $params_copy $i [expr $noparams-1]]
		set params_copy [ concat $l2 $l1 ]

		break
	    }
	    lappend errorlist $error
	}

	if { $newmin == 0 } { break }
    }

    # reorder error list
    set errorout {}
    for {set paramindex 0} {$paramindex < $noparams} {incr paramindex} {
	for {set j 0} {$j < $noparams} {incr j} {
	    if { [lindex $params_copy $j] == [lindex $params $paramindex] } {
		lappend errorout [lindex $errorlist $j]
	    }
	}
    }

    return $errorout
}

# get errors on list of parameters in datagroup
proc pct_get_error_list_dg_chan { chan dg delchi2 args } {
    set elist {}
    _pct_expand_args args
    foreach p $args {
	lappend elist [_pct_offset [expr {$dg-1}] $p]
    }

    set errors [_pct_get_error_list $elist $delchi2]

    set i 0
    foreach e $errors  {
	set a [lindex $args $i]
	tclout pinfo $a
	puts $chan "$a [lindex $e 0] [lindex $e 1] [lindex $e 2]  ! [lindex $e 3] (${xspec_tclout}) p=$a"
	incr i
    }
}

# get errors on variables (not relative in dg)
proc _get_error_list_chan { chan delchi2 args } {
    set errorlist [_pct_get_error_list "${args}" ${delchi2}]

    set i 0
    foreach e $errorlist  {
	set a [lindex $args $i]
	tclout pinfo $a
	puts $chan [format "%3i % .3e % .3e % .3e ! %s (%s) p=%i" $a [lindex $e 0] [lindex $e 1] [lindex $e 2]  [lindex $e 3] [string trim $xspec_tclout] $a]
	incr i
    }
}

# get profile values, and calculate errors
proc pct_profile_error { delchi2 args } {
    eval pct_profile_error_channel stdout $delchi2 $args
}

# get errors of parameters, and send output to the channel specified
proc pct_profile_error_channel { chan delchi2 args } {
    _pct_expand_args args
    set no_datagrp [_pct_get_no_dg]

    # construct list of parameters to get errors for
    set paramlist {}
    foreach param $args {
	for { set dg 0 } { $dg < $no_datagrp } {incr dg} {
	    lappend paramlist [_pct_offset $dg $param]
	}
    }

    # get the errors
    set errorlist [_pct_get_error_list $paramlist $delchi2]

    # now print out results

    # print out header for qdp
    puts $chan "skip single"
    puts $chan "read serr 1"
    puts $chan "read terr 2"

    set radii [_pct_get_radii]
    set count 0

    foreach param $args {
	tclout pinfo $param
	puts $chan "! Parameter $param (${xspec_tclout})"
	for { set dg 0 } { $dg < $no_datagrp } {incr dg} {
	    set errvals "[lindex $errorlist $count]"
	    set vals "[lrange $errvals 0 2]"
	    set flags "[lindex $errvals 3]"
	    set thisradii "[lindex $radii $dg]"
	    puts $chan "$thisradii $vals   ! $flags"
	    incr count
	}
	puts $chan "no no no no no"
    }
}

##############################################################
## Helper routines which operate on the same parameter
## in each datagroup
##############################################################

# thaw a set of parameters
proc pct_thaw { args } {
    _pct_expand_args args
    set no_datagrp [_pct_get_no_dg]

    foreach p $args {
	for { set dg 0 } { $dg < $no_datagrp } {incr dg} {
	    thaw [_pct_offset $dg $p]
	}
    }
}

# thaw list parameters in datagroup
proc pct_thaw_in_dg { dg args } {
    _pct_expand_args args

    foreach p $args {
	thaw [_pct_offset $dg $p]
    }	
}

# untie a set of parameters
proc pct_untie { args } {
    _pct_expand_args args
    set no_datagrp [_pct_get_no_dg]

    foreach p $args {
	for { set dg 0 } { $dg < $no_datagrp } {incr dg} {
	    untie [_pct_offset $dg $p]
	}
    }
}

# untie list parameters in datagroup
proc pct_untie_in_dg { dg args } {
    _pct_expand_args args

    foreach p $args {
	untie [_pct_offset $dg $p]
    }	
}

# tie a set of parameters together
proc pct_tie { args } {
    _pct_expand_args args
    set no_datagrp [_pct_get_no_dg]

    foreach p $args {
	for { set dg 1 } { $dg < $no_datagrp } {incr dg} {
	    newpar [_pct_offset $dg $p] =[_pct_offset 0 $p]
	}
    }
}

# freeze a set of parameters
proc pct_freeze { args } {
    _pct_expand_args args
    set no_datagrp [_pct_get_no_dg]

    foreach p $args {
	for { set dg 0 } { $dg < $no_datagrp } {incr dg} {
	    freeze [_pct_offset $dg $p]
	}
    }
}

# freeze list of parameters in datagroup
proc pct_freeze_in_dg { dg args } {
    _pct_expand_args args

    foreach p $args {
	freeze [_pct_offset $dg $p]
    }
}

# set parameter to value
proc pct_newpar { param val } {
    set no_datagrp [_pct_get_no_dg]

    for { set dg 0 } { $dg < $no_datagrp } {incr dg} {
	newpar [_pct_offset $dg $param] $val
    }
}

# set parameter to value in datagroup
proc pct_newpar_in_dg { dg param val } {
    newpar [_pct_offset $dg $param] $val
}

# links a set of parameters to the final parameter
proc pct_rellink { args } {
    _pct_expand_args args
    set no_datagrp [_pct_get_no_dg]

    set length [llength $args]
    if { $length < 2 } {
	puts "requires at least 2 arguments to pct_rellink"
	return
    }

    # extract which parameters are the targets
    set from_params [lrange $args 0 [expr {$length-2}]]
    set to_param [lindex $args [expr {$length-1}]]

    for { set dg 0 } { $dg < $no_datagrp } {incr dg} {
	foreach p $from_params {
	    newpar [_pct_offset $dg $p] =[_pct_offset $dg $to_param]
	}
    }
}

# links parameters within dataset with a multiplier
proc pct_rellink_mult { param1 param2 mult } {
    set no_datagrp [_pct_get_no_dg]

    for { set dg 0 } { $dg < $no_datagrp } {incr dg} {
	newpar [_pct_offset $dg $param1] =[_pct_offset $dg $param2]*[expr {$mult*1.0}]
    }
}

############################################################
## Fit quality routines
############################################################

# calculate the chi2 contribution from each datagroup
proc pct_chi2 { datagroup } {
    tclout plot delchi y $datagroup

    set sum 0
    foreach val $xspec_tclout {
	set sum [expr {$sum + $val*$val}]
    }
    return $sum
}

# count number of channels plotted
proc _pct_count_chan { datagroup } {
    tclout plot delchi y $datagroup
    set count 0
    foreach v $xspec_tclout {
	incr count
    }
    return $count
}

# list the chi2 contribution from each datagroup
proc pct_list_chi2 { } {
    set no_datagrp [_pct_get_no_dg]

    tclout stat
    set totchi2 $xspec_tclout
    puts "dg\tchi2\tchi2/chan\tredc\tfrac chi2"
    for { set dg 1 } {$dg <= $no_datagrp} {incr dg} {
	set chi2 [pct_chi2 $dg]
	set redchi2 [pct_redchi2 $dg]
	set chan [_pct_count_chan $dg]
	set chi2chan [format %.3f [expr {$chi2/$chan}]]
	set frac [format %.3f [expr {$chi2/$totchi2}]]
	puts "$dg\t[format %.1f $chi2]\t$chi2chan\t\t[format %.3f $redchi2]\t$frac"
    }
}

# calculate the contrib to reduced chi2 from each datagroup
proc pct_redchi2 { datagroup } {
    tclout dof
    set dof $xspec_tclout

    return [expr {[pct_chi2 $datagroup]/($dof*1.0)}]
}

# make a qdp file containing the residuals of each
# datagroup
proc pct_plot_residuals { filename } {
    setplot en
    set file [open $filename w]

    set no_datagrp [_pct_get_no_dg]

    # find minimum and maximum energies
    set minx 1.0e10
    set maxx -1.0e10

    for { set dg 1 } { $dg <= $no_datagrp } {incr dg} {
	tclout plot delchi x $dg
	set val_x $xspec_tclout
	set last_val [lindex $val_x [expr {[llength $val_x] - 1}]]
	set first_val [lindex $val_x 0]
	if { $first_val < $minx } { set minx $first_val }
	if { $last_val > $maxx } { set maxx $last_val }
    }

    # write qdp headers
    puts $file "skip single"
    puts $file "read serr 1"
    puts $file "read serr 2"
    puts $file "rescale x $minx $maxx"
    puts $file "log x on"
    puts $file "col 1 on 1..${no_datagrp}"
    puts $file "plot vertical"

    # add a horizontal line at 0 for each datagroup
    for { set dg 1 } { $dg <= $no_datagrp } {incr dg} {
	puts $file "win $dg"
	puts $file "LAB  $dg POS 0.00100000005 0 \" \""
	puts $file "LAB  $dg LI  0 100 LS 2 JUS Lef"
    }

    # write out the data for each datagroup
    for { set dg 1 } { $dg <= $no_datagrp } {incr dg} {
	puts $file "! datagroup $dg"
	# get contents of residual arrays
	foreach t {x y xerr yerr} {
	    tclout plot delchi $t $dg
	    set val_$t $xspec_tclout
	}

	set no_vals [llength $val_x]
	for { set v 0 } { $v < $no_vals } {incr v} {
	    set x [lindex $val_x $v]
	    set y [lindex $val_y $v]
	    set xerr [lindex $val_xerr $v]
	    set yerr [lindex $val_yerr $v]
	    puts $file "$x $xerr $y $yerr"
	}
	puts $file "no no no no"
    }

    close $file
    return
}

# make a volume-filling-factor plot of the two temperature components
proc pct_plot_vff { T1 norm1 T2 norm2 } {
    set no_datagrp [_pct_get_no_dg]
    set radii [_pct_get_radii]

    for { set dg 0 } { $dg < $no_datagrp } {incr dg} {
	set T1v [_pct_get_param $dg $T1]
	set T2v [_pct_get_param $dg $T2]
	set norm1v [_pct_get_param $dg $norm1]
	set norm2v [_pct_get_param $dg $norm2]

	# avoid divide-by-zeros (hack)
	if { $norm1v*1e7 < $norm2v } {
	    set norm1v [expr $norm2v * 1e-7]
	}

	set nratio [expr {${norm2v}/${norm1v}}]
	set tratio [expr {${T2v}/${T1v}}]
	set vff [expr {1./( 1. + $nratio * $tratio * $tratio ) }]

	puts "[lindex $radii $dg] $vff"
    }
    return
}

proc pct_plot_density { normparam  Tparam Zparam radiusscale_arcsec z} {
    # think:
    #  normparam: parameter where norm is
    #  radiusscale_arcsec: no of arcsec in radius units in shell
    #  da_Mpc: angular diameter distance (Mpc)
    #  z: redshift of cluster

    pct_plot_density_channel stdout $normparam $Tparam $Zparam $radiusscale_arcsec $z
}

###########################################################################
# Ugly routines for calculating physics with errors: must find a better way

proc _pct_ne_errors_ncalc { norm rad radiusscale_cm da_Mpc z } {
    set pi 3.141592
    set ne_nH 1.2
    set Mpc_cm [expr {3.08e18 * 1e6}]

    set rin_cm [expr {([lindex $rad 0] - [lindex $rad 1]) *
		      $radiusscale_cm}]
    set rout_cm [expr {([lindex $rad 0] + [lindex $rad 1]) *
		       $radiusscale_cm}]
    set vol_cmc [expr {4. / 3. * $pi * (pow($rout_cm,3) - pow($rin_cm,3))}]
    
    # norm=10**-14 / (4 pi (D_A*(1+z))**2) Int n_e n_H dV
    # calc ne
    set ne_sqd [expr {($norm/$vol_cmc) * 4*$pi * $ne_nH * 1e14 *
		      pow($da_Mpc * $Mpc_cm * (1.+$z), 2)}]
    set ne [expr {sqrt($ne_sqd)}]
    return $ne
}

# calculate pressure and density with errors
# (need to add other quantities)
proc pct_plot_phys_errors { channel normparm Tparm
			    radiusscale_arcsec z } {
    puts "Warning: must calculate errors on norms and Ts before running this!"

    # collect the errors on the temperatures and normalisations
    set no_datagrp [_pct_get_no_dg]
    set norm_errs ""
    set T_errs ""
    for { set dg 0 } { $dg < $no_datagrp } {incr dg} {
	set p [_pct_offset $dg $normparm]
	set v [lindex [_pct_tclout param $p] 0]
	set e [_pct_tclout error $p]

	lappend norm_errs "$v [lindex $e 0] [lindex $e 1]"

	set p [_pct_offset $dg $Tparm]
	set v [lindex [_pct_tclout param $p] 0]
	set e [_pct_tclout error $p]

	lappend T_errs "$v [expr {$v-[lindex $e 0]}] [expr {$v-[lindex $e 1]}]"
    }

    set pi 3.141592
    set Mpc_cm [expr {3.08e18 * 1e6}]

    set radii [_pct_get_radii]
    set da_Mpc [pct_angdiam_dist $z]
    puts $channel "! Angular diameter distance at z=$z is $da_Mpc Mpc"
    puts $channel "skip single"
    puts $channel "read serr 1"
    puts $channel "read terr 2"

    set rs_rad [expr {$pi * 2. * \
				   $radiusscale_arcsec / (60.*60.*360.)}]
    set rs_cm [expr {$rs_rad * $da_Mpc * $Mpc_cm}]
    set rs_kpc [expr {$rs_rad * $da_Mpc * 1000.}]

    # work out the densities
    set ne_errs ""
    puts $channel "! Density"
    for { set dg 0 } { $dg < $no_datagrp } {incr dg} {
	set norm [lindex $norm_errs $dg]
	set rad [lindex $radii $dg]

	set n0 [_pct_ne_errors_ncalc [lindex $norm 0] $rad $rs_cm $da_Mpc $z]
	set nn [_pct_ne_errors_ncalc [lindex $norm 1] $rad $rs_cm $da_Mpc $z]
	set np [_pct_ne_errors_ncalc [lindex $norm 2] $rad $rs_cm $da_Mpc $z]

	puts $channel [format "%.4e %.4e %.4e %.4e %.4e" [expr {[lindex $rad 0]*$rs_kpc}]\
		       [expr {[lindex $rad 1]*$rs_kpc}]\
		       $n0 [expr {$nn-$n0}] [expr {$np-$n0}]]
	lappend ne_errs "$n0 [expr {$nn-$n0}] [expr {$np-$n0}]"
    }
    puts $channel "no no no no no"

    # now the pressures
    puts $channel "! Pressure"
    for { set dg 0 } { $dg < $no_datagrp } {incr dg} {
	set norm [lindex $norm_errs $dg]
	set T [lindex $T_errs $dg]
	set rad [lindex $radii $dg]
	set ne [lindex $ne_errs $dg]

	set p0 [expr {[lindex $T 0]*[lindex $ne 0]}]
	set pn [expr {-sqrt( pow([lindex $T 1]/[lindex $T 0], 2) + 
			     pow([lindex $ne 1]/[lindex $ne 0], 2 ) )*$p0}]
	set pp [expr {sqrt( pow([lindex $T 2]/[lindex $T 0], 2) + 
			    pow([lindex $ne 2]/[lindex $ne 0], 2 ) )*$p0}]

	puts $channel [format "%.4e %.4e %.4e %.4e %.4e" [expr {[lindex $rad 0]*$rs_kpc}]\
		       [expr {[lindex $rad 1]*$rs_kpc}]\
			   $p0 $pn $pp]
    }
    puts $channel "no no no no no"

    # now the entropy
    puts $channel "! Entropy"
    for { set dg 0 } { $dg < $no_datagrp } {incr dg} {
	set norm [lindex $norm_errs $dg]
	set T [lindex $T_errs $dg]
	set rad [lindex $radii $dg]
	set ne [lindex $ne_errs $dg]

	set e0 [expr {[lindex $T 0]*pow([lindex $ne 0],-2./3.)}]
	set en [expr {-sqrt( pow([lindex $T 1]/[lindex $T 0], 2) +
			    pow(2./3. * ([lindex $ne 1]/[lindex $ne 0]), 2) )*
		  $e0}]
	set ep [expr {sqrt( pow([lindex $T 2]/[lindex $T 0], 2) +
			    pow(2./3. * ([lindex $ne 2]/[lindex $ne 0]), 2) )*
		  $e0}]

	puts $channel [format "%.4e %.4e %.4e %.4e %.4e" [expr {[lindex $rad 0]*$rs_kpc}]\
		       [expr {[lindex $rad 1]*$rs_kpc}]\
			   $e0 $en $ep]
    }
    puts $channel "no no no no no"
}

##############################################################################

proc _pct_calc_phys { norm T Z radiusscale_arcsec rad da_Mpc z } {
    set pi 3.141592
    set ne_nH 1.2
    set Mpc_cm [expr {3.08e18 * 1e6}]

    set radiusscale_rad [expr {$pi * 2. * \
				   $radiusscale_arcsec / (60.*60.*360.)}]
    set radiusscale_cm [expr {$radiusscale_rad * $da_Mpc * $Mpc_cm}]
    set radiusscale_kpc [expr {$radiusscale_rad * $da_Mpc * 1000.}]

    # calculate volume of shell
    set rin_cm [expr {([lindex $rad 0] - [lindex $rad 1]) * \
		       $radiusscale_cm}]
    set rout_cm [expr {([lindex $rad 0] + [lindex $rad 1]) * \
			$radiusscale_cm}]
    set vol_cmc [expr {4. / 3. * $pi * (pow($rout_cm,3) - pow($rin_cm,3))}]
    
    # norm=10**-14 / (4 pi (D_A*(1+z))**2) Int n_e n_H dV
    # calc ne
    set ne_sqd [expr {($norm/$vol_cmc) * 4*$pi * $ne_nH * 1e14 * \
			  pow($da_Mpc * $Mpc_cm * (1.+$z), 2)}]
    set ne [expr {sqrt($ne_sqd)}]

    # mass = volume * ne * (mass per electron)
    # average mass per electron for solar gas is 1.18 unified units
    # 1 amu = 8.34894315e-58 solar masses
    set gas_mass_Msun [expr {$ne * 1.18 * $vol_cmc * 8.349e-58}]
    
    # convert radius to kpc
    set r1 [expr {[lindex $rad 0]*$radiusscale_kpc}]
    set r2 [expr {[lindex $rad 1]*$radiusscale_kpc}]

    # calculate the luminosity per unit volume
    set lumin_ergps [_pct_lumin_calc $T $Z $norm $z]
    set lumin_ergpspcmc [expr {$lumin_ergps / $vol_cmc}]
    #puts "Luminosity = $lumin_ergps"
    #puts "Luminosity/unit vol = $lumin_ergpspcmc"

    # WRONG: calculate the thermal energy per unit volume ( = 3/2 * kT * n)
    # calculate the thermal energy per unit volume ( = 5/2 * kT * ntot)
    set thermal_ergpcmc [expr {2.5 * 1.381e-16 * 
			       11.60e6 * $T * ($ne+${ne}/1.2)}]
    #puts "Thermal energy/unit vol = $thermal_ergpcmc"

    # calc tcool in yrs
    set tcool_s [expr {$thermal_ergpcmc / $lumin_ergpspcmc}]
    set tcool_Gyr [expr {$tcool_s / 3.16e7 / 1e9}]

    # ratio of gas mass per yr of cooling time
    set mass_rate_Msun_yr [expr {$gas_mass_Msun / ($tcool_Gyr * 1e9)}]

    # entropy
    set entropy_keVcmsqd [expr {$T * pow($ne, -2./3.)}]

    # pressure
    set press_keVcm3 [expr {$T * $ne}]

    # return list containing physics
    return [list $r1 $r2 $ne $entropy_keVcmsqd $tcool_Gyr $press_keVcm3 $gas_mass_Msun $mass_rate_Msun_yr]
}

proc pct_plot_phys_channel { channel normparm Tparm Zparm radiusscale_arcsec z outparam } {
    set no_datagrp [_pct_get_no_dg]
    set radii [_pct_get_radii]

    set da_Mpc [pct_angdiam_dist $z]
    puts $channel "! Angular diameter distance at z=$z is $da_Mpc Mpc"

    puts $channel "read serr 1"
    for { set dg 0 } { $dg < $no_datagrp } {incr dg} {
	set norm [_pct_get_param $dg $normparm]
	set T [_pct_get_param $dg $Tparm]
	set Z [_pct_get_param $dg $Zparm]
	set rad [lindex $radii $dg]

	# routine doesn't use T and Z to calculate ne
	set r [_pct_calc_phys $norm $T $Z $radiusscale_arcsec \
		   $rad $da_Mpc $z]

	puts $channel "[lindex $r 0] [lindex $r 1] [lindex $r $outparam]"
    }
    return
}

# create density profile from norm parameter
proc pct_plot_density_channel { channel normparm Tparam Zparam radiusscale_arcsec z } {
    pct_plot_phys_channel $channel $normparm $Tparam $Zparam $radiusscale_arcsec \
	$z 2
    return
}

# calculate the cooling time from norm, T and Z params
proc pct_plot_tcool_channel { channel normparm Tparm Zparm radiusscale_arcsec z} {
    pct_plot_phys_channel $channel $normparm $Tparm $Zparm $radiusscale_arcsec \
	$z 4
    return
}

# calculate the cooling time from norm, T and Z params
proc pct_plot_entropy_channel { channel normparm Tparm Zparm radiusscale_arcsec z} {
    pct_plot_phys_channel $channel $normparm $Tparm $Zparm $radiusscale_arcsec \
	$z 3
    return
}

# calculate the pressure (in keV cm^-3) from norm, T and Z params
proc pct_plot_pressure_channel { channel normparam Tparam Zparam radiusscale_arcsec z} {
    pct_plot_phys_channel $channel $normparam $Tparam $Zparam $radiusscale_arcsec \
	$z 5
    return
}				     

# calculate the gas mass (in solar masses) from norm, T and Z params
proc pct_plot_gasmass_channel { channel normparam Tparam Zparam	radiusscale_arcsec z} {
    pct_plot_phys_channel $channel $normparam $Tparam $Zparam $radiusscale_arcsec \
	$z 6
}

# calculate the ratio of the gas mass (Msun) to the cooling time (yr)
proc pct_plot_massrate_channel { channel normparam Tparam Zparam radiusscale_arcsec z} {
    pct_plot_phys_channel $channel $normparam $Tparam $Zparam $radiusscale_arcsec \
	$z 7
}


#######################################################
## Convenient routines
#######################################################

# quick exit routine
proc q {} {
    quit
}

# show model
proc p {} {
    newpar 0
    return
}

# fit
proc f {} {
    fit
    return
}

# replace normalisations by normalisations / 100.
proc fixnorm {} {
    tclout modpar
    set no_params $xspec_tclout

    for { set p 1 } {$p <= $no_params} {incr p} {
	tclout pinfo $p
	set name [lindex $xspec_tclout 0]
	if { ${name} == "norm" } {
	    tclout param $p

	    # lrange gets round xspec12 bug
	    set par [lrange $xspec_tclout 0 5]

	    # skip frozen parameters
	    if { [lindex $par 1] < 0. } {
		continue
	    }

	    # skip linked parameters
	    if { [lindex [_pct_tclout plink $p] 0] == "T" } {
		continue
	    }

	    set n_100 [expr {[lindex $par 0]*0.01}]
	    # trap out small parameters
	    if { $n_100 < 1e-7 } {
		set n_100 1e-7
	    }
	    set newparams [lreplace $par 1 1 $n_100]
	    newpar $p $newparams
	}
    }
}

#######################################################
## Messy routines
#######################################################

# uses a subprocess of xspec to calculate results
# calculate the luminosity of gas at kT, Z, norm, redshift, H0, lambda
proc _pct_lumin_calc { kT Z norm redshift } {
    global pct_H0 pct_lambda

    set tempscriptname /tmp/temp_lumin_[pid].xcm
    set tempoutname /tmp/temp_lumin_[pid].out

    set tempscript [open $tempscriptname w]
    puts $tempscript "readline off
model mekal & $kT & & $Z & $redshift & 0 & $norm & /*
dummyrsp 0.001 10. 1000
cosmo $pct_H0 0.5 $pct_lambda
lumin 0.002 10. $redshift
tclout lumin
set f \[open $tempoutname w\]
puts \$f \[expr \[lindex \$xspec_tclout 0\]*1.\]
close \$f
exit & y"
    close $tempscript

    set throwaway [exec xspec11 $tempscriptname]
    set tempin [open $tempoutname r]
    set retn [gets $tempin]
    close $tempin

    file delete $tempscriptname
    file delete $tempoutname

    return [expr {$retn*1e44}]
}

# translation of eta function from calflx.f in xspec
#  Eta function used in Pen's approximation for luminosity distance in
#  a flat Universe
proc _pct_etafn { A Omega0 } {
    set S3 [expr {(1.-$Omega0)/$Omega0}]
    set S [expr {pow($S3, 1./3.)}]

    return [expr {2.*sqrt($S3+1)*pow(1./$A/$A/$A/$A - 0.1540*$S/$A/$A/$A +
				     0.4304*$S*$S/$A/$A + 0.19097*$S3/$A +
				     0.066941*$S*$S*$S*$S, -1./8.)}]
}

# translation to tcl of FZSQ routine in xspec (see calflx.f)
proc _pct_fzsq { REDZ Q Lambda } {
    set Z $REDZ
    set Q0 $Q

    # Cosmological constant in flat universe
    if { $Lambda > 1e-7 } {
	set Omega0 [expr {1. - $Lambda}]
	set FZ [expr {(1.+$Z)*( [_pct_etafn 1. $Omega0] -
				[_pct_etafn [expr 1./(1.+$Z)] $Omega0] )}]
	set FZSQ [expr {$FZ*$FZ}]
    } else {
	set X [expr {2.*$Z*$Q0}]
	if { $X > 1e-4 } {
	    set FZ [expr {$Q0*$Z + ($Q0-1.)*(sqrt(1.+$X)-1.)}]
	    set FZ [expr {$FZ/$Q0/$Q0}]
	    set FZ [expr {$FZ*$FZ}]
	    set FZSQ $FZ
	} else {
	    set ZSQ [expr {$Z*$Z}]
	    set ZCU [expr {$Z*$ZSQ}]
	    set FZ [expr {$Z + 0.5*$ZSQ - 0.5*$Q0*($ZSQ+$ZCU) +
			  0.5*$Q0*$Q0*$ZCU}]
	    set FZ [expr {$FZ*$FZ}]
	    set FZSQ $FZ
	}
    }

    return $FZSQ
}

# calculate luminosity distance for redshift z in Mpc
proc pct_lumin_dist { z } {
    # get current cosmology
    tclout cosmo
    set H0 [lindex $xspec_tclout 0]
    set q0 [lindex $xspec_tclout 1]
    set L0 [lindex $xspec_tclout 2]

    # work out distance
    set fz2 [_pct_fzsq $z $q0 $L0]
    set C_KM_S 299792.458
    return [expr {sqrt($fz2) * ($C_KM_S/$H0)}]
}

# get angular diameter distance for redshift z in Mpc
proc pct_angdiam_dist { z } {
    set lum_dist [pct_lumin_dist $z]
    set z1 [expr {1.+$z}]
    return [expr {$lum_dist / ($z1*$z1)}]
}

# calculate the cooling time in years for gas with temperature,
# electron density and metallicity given
# WARNING: destroys current model and data
proc cooling_time { T ne Z } {
    set z 0.01
    set kpc_cm 3.0857e21
    set pi 3.1415927
    set DA [pct_angdiam_dist $z]
    set nH [expr {$ne/1.2}]
    set vol [expr {pow($kpc_cm,3)}]

    set norm [expr {1e-14 / (4*$pi*pow($DA*$kpc_cm*1e3*(1+$z),2)) *
		    $ne * $nH * $vol}]
    model apec & ${T} & ${Z} & $z & ${norm}

    dummyrsp 0.01 50. 1000
    lumin 0.01 50 $z

    tclout lumin
    set lumin [expr {[lindex $xspec_tclout 0]*1e44}]

    set energy [expr {5./2. * 1.381e-16 * 
		      11.60e6 * $T * ($ne+$nH) * $vol}]

    set tcool_s [expr {$energy/$lumin}]
    set tcool_yr [expr {$tcool_s*3.1688765e-08}]
    return [format "%e" $tcool_yr]
}

# seed random number generator from /dev/urandom
proc seed_random { } {
    set f [open /dev/urandom]
    set b [read $f 3]
    close $f
    scan $b %c%c%c val1 val2 val3
    xset seed [expr $val1+($val2 + $val3*256)*256]
}

#######################################################
## Automatic model construction routines
#######################################################

# a warning message after construct commands
proc _pct_construct_warning {} {
    puts "\n*** REMEMBER TO SET REDSHIFT, MAJOR, MINOR AND ORIENT NOW ***\n"
}

# construct a 1t projct*phabs(mekal) model
proc pct_construct_1t_mekal { } {
    model projct*phabs(mekal) & /*

    # initial NH to 0.01
    newpar 4 0.01
    # set switch to 0
    newpar 9 0
    # untie and thaw temp, abun, norm
    pct_untie 5 7 10
    pct_thaw 5 7 10
    # set default norm and delta
    pct_newpar 10 "1e-3 1e-5"
    newpar 0
    _pct_construct_warning
    return
}

# make 1t projct*phabs(apec) model
proc pct_construct_1t_apec {} {
    model projct*phabs(apec) & /*

    # NH to 0.01
    newpar 4 0.01
    # thaw & untie T, abun, norm
    pct_untie 5 6 8
    pct_thaw 5 6 8
    # put down delta
    pct_newpar 8 "1e-3 1e-5"
    newpar 0
    _pct_construct_warning
    return
}

# make 1t projct*phabs(vapec) model
proc pct_construct_1t_vapec {} {
    model projct*phabs(vapec) & /*

    # NH to 0.01
    newpar 4 0.01
    # thaw & untie T, abun, norm
    pct_untie 5 7 20
    pct_thaw 5 7 20
    # tie together abundances
    for {set i 8} {$i<=18} {incr i} {pct_rellink $i 7}
    # put down delta
    pct_newpar 20 "1e-3 1e-5"

    newpar 0
    _pct_construct_warning
    return
}

# make 1t vmekal model
proc pct_construct_1t_vmekal {} {
    model projct*phabs(vmekal) & /*

    # NH to 0.01
    newpar 4 0.01
    # T to 3 keV
    newpar 5 3.
    # norm to 1e-3 1e-5
    newpar 23 1e-3 1e-5
    # thaw Ni, Fe, Ca, Ar, S, Si, Mg, Ne, O
    thaw 20 19 18 17 16 15 13 11 10
    # untie T, norm, C-Ni
    pct_untie 5 23 8-20

    # end
    newpar 0
    _pct_construct_warning
    return
}

# make 1t vmekal model
proc pct_construct_1t_vmekal_gaussian {} {
    model projct*phabs(vmekal+gaussian) & /*

    # NH to 0.01
    newpar 4 0.01
    # T to 3 keV
    newpar 5 3.
    # norm to 1e-3 1e-5
    newpar 23 1e-3 1e-5
    # thaw Ni, Fe, Ca, Ar, S, Si, Mg, Ne, O
    thaw 20 19 18 17 16 15 13 11 10
    # untie T, norm, C-Ni
    pct_untie 5 23 8-20

    # set gaussian
    newpar 24 1.82
    newpar 25 0
    freeze 24 25
    newpar 26 1e-5 1e-7
    pct_untie 26

    # end
    newpar 0
    _pct_construct_warning
    return
}

# make 2t projct*phabs(vapec+vapec) model
proc pct_construct_2t_vapec {} {
    model projct*phabs(vapec+vapec) & /*

    # NH to 0.01
    newpar 4 0.01
    # untie T, abun, norm
    pct_untie 5 21 7-18 23-34 20 36
    pct_thaw 7
    # tie together abundances
    for {set i 7} {$i<=18} {incr i} {pct_rellink $i [expr $i+16]}
    pct_thaw 17 18
    # put down delta
    pct_newpar 20 "1e-3 1e-5"
    pct_newpar 36 "1e-3 1e-5"
    # initialise temperature
    pct_newpar 5 0.5
    pct_newpar 21 2
    newpar 35 =19
    newpar 0
    _pct_construct_warning
    return
}

proc pct_construct_2t_vmekal {} {
    model projct*phabs(vmekal+vmekal) & /*

    # NH to 0.01
    newpar 4 0.01
    # put down delta
    newpar 23 1e-3 1e-5
    newpar 42 1e-3 1e-5
    # untie T, abun, norm
    pct_untie 5 24 8-20 27-39 23 42
    # tie together abundances
    for {set i 8} {$i<=20} {incr i} {pct_rellink [expr $i+19] $i}
    # initialise temperature
    pct_newpar 5 0.5
    pct_newpar 24 2
    # thaw Ni, Fe, Ca, Ar, S, Si, Mg, Ne, O
    #pct_thaw 20 19 18 17 16 15 13 11 10
    # tie redshifts
    newpar 40 =21
    newpar 0
    _pct_construct_warning
    return
}

# make 2t projct*phabs(apec+apec) model
proc pct_construct_2t_apec {} {
    model projct*phabs(apec+apec) & /*

    # NH to 0.01
    newpar 4 0.01
    # thaw & untie abun, T, norm
    pct_untie 5 6 8 9 10 12
    pct_thaw 5 6 8 9 10 12
    # link abundances
    pct_rellink 6 10
    # link redshifts
    pct_rellink 11 7
    # set norm delta
    pct_newpar 8 "1e-3 1e-5"
    pct_newpar 12 "1e-3 1e-5"
    pct_newpar 9 2.
    _pct_construct_warning
    newpar 0
}

# make a 2t projct*phabs(mekal) model
proc pct_construct_2t_mekal { } {
    model projct*phabs(mekal+mekal) & /*
    newpar 4 0.01
    newpar 9 0

    # link switch
    pct_rellink 15 9
    # thaw and untie parameters
    pct_untie 5 7 10 11 16
    pct_thaw 5 7 10 11 16
    # link abundances
    pct_rellink 13 7
    # link redshifts
    pct_rellink 14 8
    # set defaults
    pct_newpar 10 "1e-3 1e-5"
    pct_newpar 16 "1e-3 1e-5"
    pct_newpar 11 2.

    newpar 0
    _pct_construct_warning
    return
}

# construct a mekal+mkcflow model
proc pct_construct_mkcflow {} {
    model projct*phabs(mekal+mkcflow) & /*
    # set redshift
    newpar 8 0.01
    # link redshifts
    newpar 14 =8

    # set NH to 0.01
    newpar 4 0.01
    # set kT to 3
    newpar 5 3
    # set lowT to 0.0808
    newpar 11 0.0808
    freeze 11
    # set norm and delta
    newpar 10 1e-3 1e-5
    # set mkcflow norm
    newpar 16 0.1 1e-3

    # untie kT, Abun, norm, highT, abun, norm
    pct_untie 5 7 10 12 13 16
    pct_thaw 5 7 10 12 13 16

    # link temperatures
    pct_rellink 12 5
    # link abundances
    pct_rellink 13 7
    # link switches
    pct_rellink 9 15
    
    newpar 0
    _pct_construct_warning
    return
}

# construct a multiple temperature model (JSS specific)
proc pct_construct_mulgas {} {
    model projct*phabs(mulgas+gaussian) & /*
    # set NH
    newpar 4 0.01

    # set norms
    newpar 25 1e-3 1e-5
    newpar 28 1e-5 1e-7

    # set gaussian
    newpar 26 1.82
    newpar 27 0
    freeze 26 27

    # thaw various things
    thaw 9 10 11 13-18 22

    # untie
    pct_untie 5 7-18 22-24 25 28

    # set mekal
    newpar 20 2

    newpar 0
    _pct_construct_warning
    return
}

proc pct_construct_mekal_powerlaw {} {
    model projct*phabs(mekal+powerlaw) & /*
    # set NH
    newpar 4 0.01

    # set norms
    newpar 10 1e-3 1e-5
    newpar 12 1e-5 1e-7

    # set photon index
    newpar 11 1.5

    # set switch to 0
    newpar 9 0.

    # thaw abundance
    thaw 7

    # untie temperature, abundance, mekal norm, plaw norm
    pct_untie 5 7 10 12

    newpar 0
    _pct_construct_warning
    return
}

proc pct_construct_apec_powerlaw {} {
    model projct*phabs(apec+powerlaw) & /*
    # set NH
    newpar 4 0.01

    # set norms
    newpar 8 1e-3 1e-5
    newpar 10 1e-5 1e-7

    # set photon index
    newpar 9 1.5

    # thaw abundance
    thaw 6

    # untie temperature, abundance, mekal norm, plaw norm
    pct_untie 5 6 8 10

    newpar 0
    _pct_construct_warning
    return
}

proc pct_construct_multitemp_apec { args } {
    set m "projct*phabs("
    set minit "0 & 0 & 0 & 0.1"
    set first 1
    foreach T $args {
	if { ! $first } {
	    set m "${m}+"
	}
	set m "${m}apec"
	set minit "${minit} & $T -0.01 & =6 & =7 & 1e-5 1e-8"
	set first 0
    }
    set m "${m})"

    model $m & $minit & /*

    set index 5
    foreach T $args {
	pct_untie [expr ${index}+3]

	if { $index != 5 } {
	    pct_rellink [expr ${index}+1] 6
	} else {
	    pct_untie 6
	    pct_thaw 6
	    pct_freeze 7
	}

	set index [expr ${index}+4]
    }
}

# construct a multi temperature model made up of the listed temperature cmpts
# and optionally powerlaws
proc construct_multitemp { args } {
    set m "phabs(mekal"
    set minit "0.1 & [lindex $args 0] -0.01 & & 0.5 & 0.0183 & 0. & 1e-5 1e-8 &"

    set Ts [lrange $args 1 end]

    foreach T $Ts {
	if {$T == "p"} {
	    # powerlaw compt
	    set m "${m}+powerlaw"
	    set minit "${minit} 2 -0.01 & 1e-4 1e-6 &"
	} else {
	    # normal mekal
	    set m "${m}+mekal"
	    set minit "${minit} $T -0.01 & =3 & =4 & =5 & =6 & 1e-5 1e-8 &"
	}
    }
    set m "${m})"
    
    model $m & $minit /*
}

proc construct_multitemp_apec { args } {
    set m "phabs(apec"
    set minit "0.1 & [lindex $args 0] -0.01 & 0.5 & 0.0183 & 1e-5 1e-8 &"

    set Ts [lrange $args 1 end]

    foreach T $Ts {
	if {$T == "p"} {
	    # powerlaw compt
	    set m "${m}+powerlaw"
	    set minit "${minit} 2 -0.01 & 1e-4 1e-6 &"
	} else {
	    # normal mekal
	    set m "${m}+apec"
	    set minit "${minit} $T -0.01 & =3 & =4 & 1e-4 1e-6 &"
	}
    }
    set m "${m})"
    
    model $m & $minit /*
}

proc construct_multitemp_vapec { args } {
    set m "phabs(vapec"
    set minit "0.1 & [lindex $args 0] -0.01 & & & & & & & & & & & & & & & 1e-3 1e-5 &"

    set Ts [lrange $args 1 end]

    foreach T $Ts {
	if {$T == "p"} {
	    # powerlaw compt
	    set m "${m}+powerlaw"
	    set minit "${minit} 2 -0.01 & 1e-4 1e-6 &"
	} else {
	    # normal mekal
	    set m "${m}+vapec"
	    set minit "${minit} $T -0.01 & =3 & =4 & =5 & =6 & =7 & =8 & =9 & =10 & =11 & =12 & =13 & =14 & =15 & =16 & 1e-3 1e-5 &"
	}
    }
    set m "${m})"
    
    model $m & $minit /*
}

proc construct_multitemp_vapec_gsmooth { args } {
    set m "phabs(jgsmooth(vapec)"
    set minit "0.1 & 0 -1e-4 0 0 1e-1 1e-1 & 0 & [lindex $args 0] -0.01 & & & & & & & & & & & & & & & 1e-3 1e-5 &"

    set Ts [lrange $args 1 end]

    foreach T $Ts {
	if {$T == "p"} {
	    # powerlaw compt
	    set m "${m}+powerlaw"
	    set minit "${minit} 2 -0.01 & 1e-4 1e-6 &"
	} else {
	    # normal mekal
	    set m "${m}+jgsmooth(vapec)"
	    set minit "${minit} 0 -1e-4 0 0 1e-1 1e-1 & 0 & $T -0.01 & =5 & =6 & =7 & =8 & =9 & =10 & =11 & =12 & =13 & =14 & =15 & =16 & =17 & =18 & 1e-3 1e-5 &"
	}
    }
    set m "${m})"
    
    model $m & $minit /*
}

proc construct_multitemp_apec_range { args } {
    set m "phabs("
    set minit "0.1 & "
    set lower 0.0808

    for {set i 0} {$i < [llength $args]} {incr i} {
	set T [lindex $args $i]
	if { [expr $i+1] < [llength $args] } {
	    set upper [lindex $args [expr $i+1]]
	} else {
	    set upper ""
	}

	# add + if not first cmpt
	if {[string range $m end end] != "("} {
	    set m "${m}+"
	}

	# normal mekal
	set m "${m}apec"
	set minit "${minit} $T -0.01 $lower $lower $upper $upper & =3 & =4 & 1e-5 1e-8 &"

	set lower $T
    }
    set m "${m})"
    
    model $m & $minit /*
}

# plot norms of multitemp model
proc plot_multitemp {} {
    set numcmpts [_pct_tclout modcomp]

    set backscal [lindex [_pct_tclout backscal] 0]
    for {set c 1} {$c <= $numcmpts} {incr c} {
	set cmpt [_pct_tclout compinfo $c]

	set name [lindex $cmpt 0]
	set base [lindex $cmpt 1]

	set np -1
	if { $name == "mekal" } {
	    set T [lindex [_pct_tclout param $base] 0]
	    set np [expr {$base+5}]

	}
	if { $name == "powerlaw" } {
	    set T -1
	    set np [expr {$base+1}]
	}

	if {$np > 0} {
	    set norm [expr [lindex [_pct_tclout param $np] 0]/$backscal]
	    set err [_pct_tclout error $np]
	    set nerr [expr [lindex $err 0]/$backscal-$norm]
	    set perr [expr [lindex $err 1]/$backscal-$norm]
	    
	    puts [format "%10g  %e %e %e" $T $norm $perr $nerr]
	}
    }

}
