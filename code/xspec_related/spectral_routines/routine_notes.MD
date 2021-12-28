# Routine Notes
## dec-28-21
* redpgstat cutoff for executing the error routine was set to 3 
* ignored was used like this: ```**-0.5 1.5-2.3 10.0-**``` ... remember instrumental residuals in 1.5-2.3 range
* fit was set to 250
* parallel leven was set to 4 ... from documentation: "enable parallel processing for XSPEC ... it is recomended that you set ```max num of processes``` to the number of CPU cores on your machine ... the ```leven``` option will span up to ```max num``` processes during hte Levenburg-Marquardt fitting, specifically to perform the N independent calculations of the parameter first-order partial derivatives (N being the number of variable fit parameters) ... speed-up that one can expect is highly dependent on the model in use. For simpler models ... you will probably see little to no speed gain ... but with multicore CPUs, gains should be quite noticable when the model calculation consumes a large fraction of the overall fitting time."
* if a errorlog file exists for the seg_id, then need to get values from it. in all cases I also log the normal log file to get other parameters like source %, etc. 
* good news: although the log files from running the error routine are really messy (not sure how to extract bounds at this point), running the routine updates the values in the normal xspec so those updated values get logged when the normal log is run. Nice. 