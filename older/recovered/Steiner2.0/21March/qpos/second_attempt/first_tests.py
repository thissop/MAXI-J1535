def first_test(pds,rsp,obsid):
    # Import(s)
    #from xspec import Spectrum
    
    # Action
    obsid_list = obsid.split('_')
    id = obsid_list[0]
    gti = obsid_list[1]
    pds = (pds.replace('+++',id)).replace('+',gti)
    rsp = (rsp.replace('+++',id)).replace('+',gti)
    #s = Spectrum(pds)
    #s.show()
    print('"'+pds+'"')
    print('"'+rsp+'"')


pds_temp = "/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI+-bin.pds"
rsp_temp = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI+-fak.rsp'
first_test(pds=pds_temp,rsp=rsp_temp,obsid='1130360110_0')