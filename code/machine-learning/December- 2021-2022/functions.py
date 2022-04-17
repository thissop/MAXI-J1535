def get_plot(id: str): 
    from PIL import Image
    import requests

    url = 'https://raw.githubusercontent.com/thissop/MAXI-J1535/main/code/xspec_related/qpo_routines/full_aggregation/plot_dists/quad-panels/'
    url += id + '.png'
    im = Image.open(requests.get(url, stream=True).raw)

    return im