# How to Install XSPEC on WSL 

1. First have WSL installed on windows (of course)
2. Download source code from this [link](https://heasarc.gsfc.nasa.gov/lheasoft/download.html)
    * Make sure to select the source code option for ``` PC - Microsoft Windows WSL (Windows Subsystem For Linux)```
    * For ease of future use, select ```All`` underneath ```STEP 2 - Download the desired packages```
3. Enter WSL, execute this string of commands: 
```sh
sudo apt-get -y install libreadline-dev
sudo apt-get -y install libncurses5-dev
sudo apt-get -y install ncurses-dev
sudo apt-get -y install curl
sudo apt-get -y install libcurl4
sudo apt-get -y install libcurl4-gnutls-dev
sudo apt-get -y install xorg-dev
sudo apt-get -y install make
sudo apt-get -y install gcc g++ gfortran
sudo apt-get -y install perl-modules
```
4. Then, from WSL, navigate by combination of ls and cd to directory in which the downloaded heasoft ```tar.gz``` file is. 
5. Execute the command ```tar -xf archive.tar.gz``` where ```archive.tar.gz``` is replaced with the name of the file you downloaded from 
6. Then follow the steps in Nick the space cowboy's video ([linked here](https://www.youtube.com/watch?v=3-gobnSEuDo))

    a. Navigate to ```heasoft-6.29/BUILD_DIR``` and execute this command: ```./configure > config.txt 2>&1```
        
      * Note: the way that I am executing these commands will only give user control of the terminal back once the task has been completed (credit to nick the space cowboy). This is not the exact way that it is done in the NASA guide.
        
      * Also Note: if you want to watch the progress of any task associated with a log file, open up a new session, navigate to the directory with the log file, and type in ```tail -f filename``` 
        
    b.  Once the last step is complete, enter this command (I belive this step takes the longest): ```make > build.log 2>&1```
    
    c. Finally, execute this command in the same directory: ```make install > install.log 2>&1```
    
    
    * Note: you will have to work with an odd file path structure within wsl. Once you're in WSL, get to the directory containing the x86_64 file and type in the command ```pwd```. The resultant path should be the path you give to the aliase.

7. To edit the settings in ```.bashrc```, open up ```cmd``` and type in ```bash```. Then type in ```cd```. Then type in ```nano .bashrc```
8. Paste in the modified commands from nick the spacecowboy, then save (ctrl+s) and exit (f-12)
   * On my computer they look like this: 
   ```sh
   export HEADAS=pwd/heasoft-6.29/x86_64-pc-linux-gnu-libc2.31/
   . $HEADAS/headas-init.sh
   alias heainit=". $HEADAS/headas-init.sh"
   ```
   
   Where ```pwd``` was set to ```/mnt/c/Users/Research/Downloads```
   
10. Heasoft (and xspec) should be good to go

All in all, from starting to download the source file from NASA to making sure everything could run took me about four and a half hours. 
