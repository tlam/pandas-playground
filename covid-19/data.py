import requests


urls = [
    {
        'filename': 'recovered.csv',
        'url': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'
    },
    {
        'filename': 'confirmed.csv',
        'url': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
    },
    {
        'filename': 'deaths.csv',
        'url': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
    }
]

for url_data in urls:
    local_filename = f"fixtures/{url_data['filename']}"
    with requests.get(url_data['url']) as response:
        with open(local_filename, 'wb') as fp:
            fp.write(response.content)
