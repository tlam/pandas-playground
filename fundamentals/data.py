import re

import pandas as pd


class Sal(object):

    def __init__(self):
        self.df = pd.read_csv('fundamentals/fixtures/sal.csv')
        self.df.dropna(subset=['Annual Base Pay', 'Location'], inplace=True)
        self.df['Years of Experience'].fillna('0', inplace=True)

    def clean_amount(self, value):
        replacements = [',', ' ']
        for ch in replacements:
            value = value.replace(ch, '')

        search_object = re.search(r'\d+(\.\d+)?', value)
        if search_object:
            value = search_object.group()
        else:
            value = '0'

        return float(value.strip())

    def rename_location(self, value):
        """
        Rename some common locations under one name
        For example Bay Area, San Francisco and SF should all
        fall under San Francisco
        """
        location_mapping = {
            'calgary, ab': 'calgary',
            'calgary, alberta': 'calgary',
            'calgary, canada': 'calgary',
            'edmonton, ab': 'edmonton',
            'edmonton, alberta, canada': 'edmonton',
            'chicago il': 'chicago',
            'chicago, il': 'chicago',
            'montreal, canada': 'montreal',
            'montreal, qc': 'montreal',
            'montreal, qc, canada': 'montreal',
            'montreal, quebec, canada': 'montreal',
            'brooklyn': 'new york',
            'new york city': 'new york',
            'new york city, ny': 'new york',
            'new york, new york': 'new york',
            'new york, ny': 'new york',
            'bay area': 'san francisco',
            'san francisco, ca': 'san francisco',
            'sf': 'san francisco',
            'sf bay area': 'san francisco',
            'seattle, usa': 'seattle',
            'seattle, wa': 'seattle',
            'seattle, wa usa': 'seattle',
            'seattle, washington': 'seattle',
            'toronto, canada': 'toronto',
            'toronto, on': 'toronto',
            'toronto, ontario': 'toronto',
            'toronto, ontario, canada': 'toronto',
            'vancouver bc': 'vancouver',
            'vancouver, bc': 'vancouver',
            'vancouver, ca': 'vancouver',
            'vancouver, canada': 'vancouver',
        }
        return location_mapping.get(value, value)

    def location_data(self, locations):
        self.df['Location'] = self.df['Location'].str.lower()
        self.df['Location'] = self.df['Location'].apply(self.rename_location)
        city_df = self.df[self.df['Location'].isin(locations)]
        salary_key = 'Annual Base Pay'
        city_df[salary_key] = city_df[salary_key].apply(self.clean_amount).astype(float)
        city_df = city_df[(city_df[salary_key] > 20000) & (city_df[salary_key] < 500000)]

        print city_df[salary_key].describe()
        median = city_df[salary_key].median()
        print median

        stats = city_df[salary_key].describe().to_dict()
        stats['median'] = median
        output = {
            'graph_data': [],
            'stats': stats,
        }
        data = city_df[['Years of Experience', salary_key]].to_dict()
        graph_data = [['Years', 'Salary']]
        years = data['Years of Experience']
        pay = data[salary_key]
        for key, year in years.items():
            graph_data.append([year, pay[key]])

        output['graph_data'] = graph_data
        return output

if __name__ == '__main__':
    sal = Sal()
    '''
    location_data(df, 'New York')
    location_data(df, ['Bay Area', 'San Francisco', 'SF'])
    location_data(df, 'Seattle')
    location_data(df, 'Chicago')
    '''
    sal.location_data(['new york'])
