heainit
xspec
cd /ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/sources/GRS_1915+105/qpo/external_PDS/80701-01-54-02
data power_0_249.pha
model loren
0


freeze 1
query yes

fit

editmod loren+loren 
2.752
0.33084
13.423
show param
freeze 4-6
fit
ignore **-0.1
ignore 10.0-**
cpd /ps
setplot energy
plot ldata
cd /ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/manuscript/figures/individual/figure_5
iplot
label bottom Frequency (Hz)
label left Power (Leahy Normalized)
label top
font roman
t off
View 0.12 0.12
rescale x 0.1 10
hard  /ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/manuscript/figures/individual/figure_5/80701-01-54-02[fig-5-pds-data].ps/ps
80701-01-54-02[pds-data]/ps
80701-01-54-02[pds-data].ps/ps
quit
plot model
iplot
label top
font roman
t off
label X Frequency (Hz)
label Y Power (Leahy Normalized)
View 0.12 0.12
csize 2.0
rescale x 0.1 10
hard  /ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/manuscript/figures/individual/figure_5/80701-01-54-02[fig-5-pds-model].ps/ps
80701-01-54-02[fig-5-pds-model]/ps
80701-01-54-02[fig-5-pds-model].ps/ps
quit
model none
data none
cd /ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/sources/GRS_1915+105/qpo/external_PDS/50703-01-28-01
data power_0_249.pha
model loren
0


freeze 1
query yes

fit

editmod loren+loren 
3.09627
0.44462
11.74815
show param
freeze 4-6
fit
ignore **-0.1
ignore 10.0-**
cpd /ps
setplot energy
plot ldata
cd /ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/manuscript/figures/individual/figure_5
iplot
label bottom Frequency (Hz)
label left Power (Leahy Normalized)
label top
font roman
t off
View 0.12 0.12
csize 2.0
rescale x 0.1 10
hard  /ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/manuscript/figures/individual/figure_5/50703-01-28-01[fig-5-pds-data].ps/ps
50703-01-28-01[pds-data]/ps
50703-01-28-01[pds-data].ps/ps
quit
plot model
iplot
label top
font roman
t off
label X Frequency (Hz)
label Y Power (Leahy Normalized)
View 0.12 0.12
csize 2.0
rescale x 0.1 10
hard  /ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/manuscript/figures/individual/figure_5/50703-01-28-01[fig-5-pds-model].ps/ps
50703-01-28-01[fig-5-pds-model]/ps
50703-01-28-01[fig-5-pds-model].ps/ps
quit
model none
data none
cd /ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/sources/GRS_1915+105/qpo/external_PDS/50703-01-24-01
data power_0_249.pha
model loren
0


freeze 1
query yes

fit

editmod loren+loren 
3.13126
0.48859
11.15358
show param
freeze 4-6
fit
ignore **-0.1
ignore 10.0-**
cpd /ps
setplot energy
plot ldata
cd /ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/manuscript/figures/individual/figure_5
iplot
label bottom Frequency (Hz)
label left Power (Leahy Normalized)
label top
font roman
t off
View 0.12 0.12
csize 2.0
rescale x 0.1 10
hard  /ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/manuscript/figures/individual/figure_5/50703-01-24-01[fig-5-pds-data].ps/ps
50703-01-24-01[pds-data]/ps
50703-01-24-01[pds-data].ps/ps
quit
plot model
iplot
label top
font roman
t off
label X Frequency (Hz)
label Y Power (Leahy Normalized)
View 0.12 0.12
csize 2.0
rescale x 0.1 10
hard  /ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/manuscript/figures/individual/figure_5/50703-01-24-01[fig-5-pds-model].ps/ps
50703-01-24-01[fig-5-pds-model]/ps
50703-01-24-01[fig-5-pds-model].ps/ps
quit
model none
data none
quit
y
