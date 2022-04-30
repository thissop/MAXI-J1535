from astroquery.heasarc import Heasarc
heasarc = Heasarc()
mission = 'rxte'
table = heasarc.query(bibcode='2015MNRAS.447.2059M')
print(table)