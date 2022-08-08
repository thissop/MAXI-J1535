def get_rxte_link(obsid):
    pid = obsid[:5]
    # Calculates AO number according to obsid
    if int(pid[:2]) < 90:
        ao = 'AO'+pid[0]
    else:
        ao = 'AO'+str(int(pid[1])+9)

    # P-id of the observation according to obsid
    pid = 'P'+pid

    # obsid to download as a tar.gz file
    tarfile = obsid+'.tar.gz'

    # start  FTP connection
    link = 'heasarc.gsfc.nasa.gov/FTP/xte/data/archive/'

    # path to obsid
    path = f'{link}{ao}/{pid}/{obsid}/pca/'

    # quit FTP connection
    print(path)

obsid = '92023-01-52-10'
get_rxte_link(obsid)