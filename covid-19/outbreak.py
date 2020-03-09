"""
TODO:
Merge last column of each csv
Calculate Active in new column
"""

from datetime import datetime
import csv

import pandas as pd



class Outbreak(object):
    CITY = 'city'
    COUNTRY = 'country'
    CONFIRMED = 'confirmed'
    RECOVERED = 'recovered'
    FILE_TYPES = {
        CONFIRMED: 'fixtures/confirmed.csv',
        RECOVERED: 'fixtures/recovered.csv'
    }

    def __init__(self, city, country):
        self.city = city
        self.country = country

    def calculate(self, data_type):
        if data_type == self.CITY:
            column = 'Province/State'
            entity = self.city
        else:
            column = 'Country/Region'
            entity = self.country

        output = {
            'column': column,
            'entity': entity
        }
        for data_type, csv_path in self.FILE_TYPES.items():
            csv_path = self.FILE_TYPES[data_type]
            confirmed_df = pd.read_csv(csv_path)
            entity_df = confirmed_df[confirmed_df[column].isin([entity])]
            latest = entity_df[entity_df.columns[-1]]
            output[data_type] = {
                'value': latest.sum(),
                'timestamp': datetime.strptime(latest.name, '%m/%d/%y')
            }
        return output

    def report(self):
        for data_type in [self.COUNTRY, self.CITY]:
            data = self.calculate(data_type)
            last_date_recorded = data[self.CONFIRMED]['timestamp']
            confirmed = data[self.CONFIRMED]['value']
            recovered = data[self.RECOVERED]['value']

            print(f"{data['column']}: {data['entity']} on {last_date_recorded}")
            print(f'Active: {confirmed - recovered}')
            print(f'Recovered: {recovered} {recovered*100/confirmed:.2f}%')


if __name__ == '__main__':
    city = 'Toronto, ON'
    country = 'Canada'
    outbreak = Outbreak(city, country)
    outbreak.report()
