{#} {

> NOTE: this file is not going to work if you try to run it
> i use it to copy and paste tcl snippets (and to increase tcl portion 
> of the repository :INSANETROLL:)

> I believe that this is the correct format for multi line comments...
> the rest of this file will contain snippets denoted by double hash-tag 
"headers"

} 

## set _pct_get_error routine variable example ##

set error_array [_pct_get_error {} 2.706]

## write array items to file ##

set fo [open test.txt w]
foreach item $array_name {
    puts $fo $item
}
close $fo

## replace multiple spaces in a string with a single comma ## 

set string "boy    cat  dog" 
regsub -all {\s+} $string ,

## write array items to file after replacing spaces with comma ##

set error_log_file [open test.txt w] 
set header_string "value,lower_err,upper_err,err_str" 
puts $error_log_file $header_string
foreach item $error_array {
    set item [join $item ,]
    puts $error_log_file $item
}
close $error_log_file

## mixed xspec/tcl get red. pg stat and try to do something with it

tclout stat
scan $xspec_tclout "%f" pgstat
tclout dof')
scan $xspec_tclout "%f" dof
set redpgstat [expr $pgstat / $dof]

## thus full tcl/xspec snippet for running and logging eror routine ##

tclout stat
scan $xspec_tclout "%f" pgstat
tclout dof')
scan $xspec_tclout "%f" dof
set redpgstat [expr $pgstat / $dof]
if {$redpgstat < 3} {
    set error_log_file [open test.txt w] # need to set this with python prior
    set header_string "value,lower_err,upper_err,err_str" 
    puts $error_log_file $header_string
    foreach item $error_array {
        set item [join $item ,]
        puts $error_log_file $item
    }
    close $error_log_file
}

### Old tcl/xspec error routine that only works with default error ...mix of python in here too ###

commands.append('set errorfile [open "'+errorlog_file+'" a+]')
commands.append('puts $errorfile "param_num,lower_bound,upper_bound,error_string"')
# See if red. pgstat < 2, if so do error routine
commands.append("if {$redpgstat < 2} {")
for param_num in [2, 3, 4, 9]: 
    commands.append('error 1. '+str(param_num))
    commands.append('tclout error ' +str(param_num))
    commands.append('set tclout_error_str [join $xspec_tclout ,]') # this isn't working
    commands.append('set param_str '+str(param_num)+',')
    commands.append('set error_string $param_str$tclout_error_str')
    commands.append('puts $errorfile $error_string')

# in place of error file
commands.append("} else {")
commands.append('puts $errorfile ",,,"') # NaN-ing it
commands.append('puts $errorfile ",,,"')
commands.append('puts $errorfile ",,,"')
commands.append('puts $errorfile ",,,"')
commands.append("}")

commands.append('close $errorfile')