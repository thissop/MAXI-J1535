# MAXI-J1535
## About this project

### Miscellaneous Notes
* Keep a google colab session from disconnecting by either adding this snippet of code in the google console (via inspect element): 

<pre><code> 
function ConnectButton(){
  console.log("Connect pushed"); 
  document.querySelector("#top-toolbar > colab-connectbutton").shadowRoot.querySelector("#connect").click() 
}
setInterval(ConnectButton,60000);
</code></pre> 

* Or by adding this snippet of code ```while True:pass``` in a cell after the cell you are currently running and running it in queue. 

* To use the spiral error search ```tcl``` routine, first enter ```source common.tcl```. Then enter something like ```_pct_get_error_list {1 2 3 4} 2.71``` where `1` through `4` are the parameter numbers and `2.71` is the critical chi-squared. 

* Critical values for common cases (from [Avni 1979](https://ui.adsabs.harvard.edu/abs/1976ApJ...210..642A/abstract)):  
![criticals](https://raw.githubusercontent.com/thissop/MAXI-J1535/71aa197c8c195a133ed05c4321c03622db93d3d1/documentation/images/avni_criticals.png?token=AQN5JTZ4SQL5IP5LZYJC7I3BUZRIA)

* **Large File Storage:** from now on, I am going to store large files (> ~50 mb) outside of GitHub (e.g. in GoogleDrive) as well as locally in a directory outside of the repository they're used in (becaues GitHub will not allow files >100 mb). They will be kept under the local directory ```Documents/GitHub/lfs``` (where ```lfs``` stands for "large file storage"). 

* Current ensemble model:  
![flowchart]()

## About this repo
![Visualization of this repo](./diagram.svg)

