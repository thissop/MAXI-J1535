# xspectoolsv3
A handy compendium of useful functions I've written to make working with XSPEC more expeditious. 
#### General conventions and things to note
  - Functions generally return string values, rather than the numerical fit results from XSPEC, because the observation id (which is itself immediately followed by a colon) precedes the fit result in an output value. An example of this in the form of an  output from the returnDates() function: ```'1050360103:58005.3035185'```, where the first term is the obsid and the second is the date value returned from the obsid's .fits file. I decided to format all results like this to make it easier to combine findings from multiple functions, e.g. simultaneous plotting of fit results, hardness ratios, and count rates all on dates found from the returnDates() function. 
  - ```obsid``` is short for observation ID (`ObsID` in NICER nomenclature, ```obsid``` in the code). These values should be strings. Example: ```1130360177```.
  - ```gti``` is short for ```good time interval``` and refers to the good time interval of a NICER observation (typical NICER observations have durations of a few ksec and are often subdivided into data segments due to gaps caused by the orbit of the ISS, etc.). These values should be strings. Example: ```1```. 
  - ```seg_id``` is short for ```segment_id``` and contains both the ```obsid``` and ```gti``` of a data file, which are separated in a string by a colon. These values should be strings. Example: ```1130360177:1```.
  - Unless specifically said otherwise, the ```IDs``` parameter refers to a list of ```seg_id``` values in these functions. 
#### Requirements
- Astropy
- Numpy
- Python (3)
## returnDates()
This function iterates through a list of ```seg_id``` strigs and retrieves the ```MJDSTART``` values from their ```.fits``` files. It also works with ```.jsgrp``` data files. 
- **Parameters**
  - IDs: list of ```seg_ids```.  
  - path_temp: path template for the ```.fits``` or ```.jsgrp``` files. Note: the ```obsid``` value in this string should be replaced by ```++++++++++``` and the ```gti``` value should be replaced by a single ```+``` (even if the ```gti``` value is more than ```9```. This is true for all of the functions and won't be repeated. Example: ```path_temp='/home/++++++++++/jspipe/js_ni++++++++++_0mpu7_silver_GTI+.jsgrp'```.
  - out_list: the name of the predefined list into which ```date_strings``` should be deposited (the ```date_string``` values look like this: ```obsid:mjdstart```). 
- **Example:**
```python
#Declare prerequisites
idlist = ['1130360183:0','1130360184:10','1130360185:2']
example_path = '/home/++++++++++/jspipe/js_ni++++++++++_0mpu7_silver_GTI+.jsgrp'
mjds = []
#Action
returnDates(IDs=idlist,path_temp=example_path,out_list=mjds)
```
## returnFitResults()
I wrote this function to sweep through a directory of log files and retrieve the fitted parameter values from each. XSPEC log verbosity should have been set to ```10``` during the fitting routine to ensure this function works properly. 
- **Parameters:**
  - IDs: same as always. 
  - path_temp: same as always. 
  - fit_stat: this should be a string which declares what fit stat was used. Right now it can only take 'pgstat' because I've only been working with the pg-statistic. 
  - fit_params: this should be a list of string values which tell the function which parameters to retrieve and how to retrieve them. Each element in this list should be set up like this: 'component:parameter:line_index', where 'component' is the name of the parameter's model component in the log file (e.g. 'relxill'), where 'parameter' is the name of the parameter (e.g. 'logxi'), and where 'line_index' is the pythonic index of where the parameter's value is found in the line it's logged in. Here is an example XSPEC line to illustrate this 'line_index' concept: 
```#  19    4   relxill    logxi               0.338605     +/-  0.298524```   
This function replaces all instances of whitespace in this line with single commas, and then splits the line into a list on these commas. The index of the logxi value in this line is then 5. Hence, the fit_params element for logxi would be ```'relxill:logxi:5'```. 
  - out_lists: this should be a list of variable names for the predefined lists into which the fit results should be deposited. They should be in the same order as the fit_params they correspond to. 
  - rfsl: this should be set to the name of the predefined list into which the reduced fit statistics should be deposited. 
- **Example:**
```python
#Declare prerequisites
gammas = []
scat_fracs = []
Tins = []
redpgs = []
example_path = '/home/++++++++++.log'
idlist = ['1130360183:0','1130360184:10','1130360185:2']
#Action
returnFitResults(IDs=idlist,path_temp=example_path,fit_stat='pgstat',fit_params=['simpl:Gamma:5','simpl:FracSctr:5','diskbb:Tin:6'],out_lists=[gammas,scat_fracs,Tins],rfsl=redpgs)
```
## bestErrorRoutine()
This function, as the name implies, is the best function I've written for handling, aggregating, and processing (oo the oxford comma lol...I guess the SAT is getting to my grammar :p) XSPEC error results so far. It's preferable that XSPEC log verbosity was set to ```5``` for the error log files fed to this function. Note: rather than deposite values into parameter-defined lists, this function returns six lists, so you access them by function index (see Note on outputs). ```CWZ``` and ```cwz``` refer to values that were consistent with 0 within errors. ```PHUZ``` stands for 'ParameterHitUpperZero' and means a parameter was pegged at its upper limit; ```PHLZ``` stands for 'ParameterHitLowerZero' and means a parameter was pegged at its lower limit.  
- **Parameters**
  - IDs: same as always.  
  - path_temp: same as always. 
  - param_num: integer, model parameter number of the parameter in question. 
  - date_strings: an output list from returnDates(), with the same length as IDs
  - value_strings: an output list from returnFitResults(), with the same length as IDs
- **Note on outputs**
  - ```bestErrorRoutine(...)[0]```: dates for good error points
  - ```bestErrorRoutine(...)[1]```: values for good error points
  - ```bestErrorRoutine(...)[2]```: good error array (dimensions set for yerr of matplotlib)
  - ```bestErrorRoutine(...)[3]```: dates for cwz error points
  - ```bestErrorRoutine(...)[4]```: values for cwz points
  - ```bestErrorRoutine(...)[5]```: cwz error array (dimensions set for yerr of matplotlib) ----- PHLZ/PHUZ values are set to 0.0
- **Example:**
```python
#Declare prerequisites
idlist = [] #pretend this is populated
mjds = [] #pretend this is populated
path_template = '/home/++++++++++_+.log'
values = [] #pretend this is populated

error_func = best_error_routine(IDs=idlist,path_temp=path_template,param_num=2,date_strings=mjds,value_strings=values)
cwz_dates = error_func[3]
cwz_vals = error_func[4]
```

# XSPECtools
A handy compendium of useful functions I've written to make working with XSPEC more expeditious. 
#### General conventions and things to note
- All functions utilize ```if os.path.exists()==True:``` as a check to make sure files exist before attempting to open them. 
- All functions return string values, rather than the numerical fit results from XSPEC, because the observation id (which is itself immediately followed by a colon) precedes the fit result in an output value. An example of this in the form of an example output from the returnDates() function: ```'1050360103:58005.3035185'```, where the first term is the obsid and the second is the date value returned from the obsid's .fits file. I decided to format all results like this to make it easier to combine findings from multiple functions, e.g. simultaneous plotting of fit results, hardness ratios, and count rates all on dates found from the returnDates() function. 
- For both returnCountRates() and returnHardnessRatios(), here's the approach I recommend taking for defining the intervals: ignore the keV regions you want to ignore (e.g. ```ignore **-0.5 10.0-**```), and then execute ```show noticed```. For the example output ```Noticed channels: 22-254```, you would set your channel interval to ```['22:254']```.
#### TRANSITION NOTES
- Add the XSPECtoolsv2 to nicer_tools, rename it, rename documentation. 
- **Nomenclature:**
  - From now on, the term ```'obs_id'``` refers to identifier for individual NICER observations, like ```1050360103```.
  - Since NICER observations are often multiple ks in duration, they are subdivided into smaller segments—due to gaps caused by the orbit of the ISS—which are ranked by time into good time intervals (GTI).```'seg_id'``` values contain information which identifies both the NICER observation and GTI numbers of a data file, in the form ```'[obs_id]_[gti]'```. For example, the ```'seg_id'``` for the fourth GTI of the NICER observation ```1050360103``` would be ```'1050360103_3'``` (GTI intervals start at zero—like python indices). 
  - gti refers to the good time interval of the data file. It's equal to ```seg_id.split('_')[1]```. 
  - By the time this transition is done, returnHardnessRatios() and returnCountRates() will both return background counts corrected values. 🤪
  - The old returnHardnessRatios() and returnCountRates() are completely depreciated at this point. The old returnHardnessRatios() function was returning ratios of counts, not count rates 😂.
  - Note that returnCountRates() and returnHardnessRatios() are both deadtime and detector on/off time corrected
- **TO DO:**
  - Finalize returnCountRates() and returnHardnessRatios(). Change their intervals such that you input the keV ranges and the channels ignored are the ```min(range)*10``` and ```max(range)*10```. It may not be 10...just change it that way. 
#### Requirements
- Astropy 3.3.0 or later
- Matplotlib 3.1.0 or later
- Numpy 1.17.0 or later
- Python 3.7 or later
###### Note to self: All of these functions and their documentation notes are going to have to change if/when I update them to fit more than the "default" data file for each observation.
## returnConfidenceIntervals()
This function sweeps through a directory of log files to retrieve error results. XSPEC log verbosity should have been set to 5 to ensure this function works properly. 
- **Parameters:**
  - IDs: this should be a list of string value observation IDs for all the data files you want to return fit results from. 
  - path_temp: this should be the template path for all of the log files, with the observation ID replaced with a string '++++++++++' value (because I wrote the function to replace '++++++++++' with the observation ID for each observation ID in the IDs list). 
  - param_nums: this should be a list of integers which represent the numbers of each parameter of interest in the fitted model. 
  - out_lists: this should be a list of the predefined names of the lists into which the confidence intervals should be deposited. 
  - NOTE TO SELF: When u finish documentation for this function, make sure you discussed PHUZ, PHLZ, NaN, plt.errorbar (which is why lower end of ci is returned as abs(val) not val becuase plt.errorbar requires all values to be positive). 
- **Example:**
```
#Declare prerequisites  
gammas = []
scatfracs = []
Tins = []
pathTemp = '/home/error++++++++++.log' 
idlist = ['1130360183','1130360184','1130360185'] 
#Action
returnConfidenceIntervals(IDs=idlist,pathtemp=pathTemp,pnumbers=[5,6,8],listnames=[gammas,scatfracs,Tins]) 
```
## returnCountRates()
This function returns the net count rates from every observation's .fits file. 
- **Parameters**
  - IDs: same as always. 
  - path_temp: same as always. 
  - channel_ints: This should be a list of strings which denote what channels to draw counts from. If you wanted to draw counts from multiple channel ranges, include multiple elements in this list. Each element should be formatted as such: 'lower_channel:upper_channel', where lower_channel is the number of the lowest channel you want to extract counts from, and upper_channel is the highest channel you want to extract counts from (so think of it as a closed—rather than open—interval). 
  - out_list: this should be set to the name of a predefined list into which count rates should be deposited. 
- **Example**:
```
#Declare prerequisites
idlist = ['1130360183','1130360184','1130360185']
example_path = '/home/++++++++++.jsgrp' 
count_rates = []
returnCountRates(IDs=idlist,path_temp=example_path,channel_ints=['1:26','78:109','200:258'],out_list=count_rates)
```
## returnDates()
This function enters .fits files for the observation dates. I believe it can only work with the custom processed NICER data I've been working with (hence the '.jsgrp' filetype in the example). 
- **Parameters**
  - IDs: same as always. 
  - path_temp: same as always. 
  - out_list: the name of the predefined list into which results should be deposited. 
- **Example:**
```
#Declare prerequisites
idlist = ['1130360183','1130360184','1130360185']
example_path = '/home/++++++++++.jsgrp'
hjds = []
#Action
returnDates(IDs=idlist,path_temp=example_path,out_list=hjds)
```
## returnFitResults()
I wrote this function to sweep through a directory of log files and retrieve the fitted parameter values from each. XSPEC log verbosity should have been set to 10 to ensure this function works properly. 
- **Parameters:**
  - IDs: same as always. 
  - path_temp: same as always. 
  - fit_stat: this should be a string which declares what fit stat was used. Right now it can only take 'pgstat' because I've only been working with the pg-statistic. 
  - fit_params: this should be a list of string values which tell the function which parameters to retrieve and how to retrieve them. Each element in this list should be set up like this: 'component:parameter:line_index', where 'component' is the name of the parameter's model component in the log file (e.g. 'relxill'), where 'parameter' is the name of the parameter (e.g. 'logxi'), and where 'line_index' is the pythonic index of where the parameter's value is found in the line it's logged in. Here is an example XSPEC line to illustrate this 'line_index' concept: 
```#  19    4   relxill    logxi               0.338605     +/-  0.298524```   
This function replaces all instances of whitespace in this line with single commas, and then splits the line into a list on these commas. The index of the logxi value in this line is then 5. Hence, the fit_params element for logxi would be ```'relxill:logxi:5'```. 
  - out_lists: this should be a list of variable names for the predefined lists into which the fit results should be deposited. They should be in the same order as the fit_params they correspond to. 
  - rfsl: this should be set to the name of the predefined list into which the reduced fit statistics should be deposited. 
- **Example:**
```
#Declare prerequisites
gammas = []
scat_fracs = []
Tins = []
redpgs = []
example_path = '/home/++++++++++.log'
idlist = ['1130360183','1130360184','1130360185']
#Action
returnFitResults(IDs=idlist,path_temp=example_path,fit_stat='pgstat',fit_params=['simpl:Gamma:5','simpl:FracSctr:5','diskbb:Tin:6'],out_lists=[gammas,scat_fracs,Tins],rfsl=redpgs)
```
## returnHardnessRatios()
This function returns hardness ratios for all requested files in a directory. 
- **Parameters:**
  - IDs: same as always.
  - path_temp: same as always
  - n_channel_ints: this should be a list whose elements denote the channel intervals from which the counts for the numerator (of the hardness ratio) will be drawn from (the lower and upper channel limits should be separated by a colon, as per usual): ```n_channel_ints = ['101:254']```
  - d_channel_ints: same as above, except elements denote the channel intervals from which the counts for the denominator will be drawn from. 
  - out_list: this should be the name of the predefined list into which the hardness ratios will be deposited. 
- **Example:**
```
#Declare prerequisites
example_path = '/home/++++++++++.jsgrp'
idlist = ['1130360183','1130360184','1130360185']
hardness_ratios = []
#Action
returnHardnessRatios(IDs=idlist,path_temp=example_path,n_channel_ints=['101:254'],d_channel_ints=['22:54','79:99'],out_list=hardness_ratios) 
```
   ###### * Note: d_channel_ints=['22:54','79:99'] means the sum of the counts in channels 22-54 and 79-99 will be used as the denominator, aka the soft band counts (in NICER data these channel intervals correspond to the 0.5-1.5 and 2.2-3 keV bands).
