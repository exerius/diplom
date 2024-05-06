import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import sqlalchemy

rng = np.random.default_rng(42)

engine = sqlalchemy.create_engine("postgresql://postgres:123@localhost:5432/postgres")

os = ['Windows', 'OS X', 'Linux', 'Android', 'IOS', 'Other']

dataset = pd.DataFrame(columns=['id', 'sex', 'age', 'os', 'region', 'category_1', 'mark_1',
                                'category_2', 'mark_2', 'category_3', 'mark_3'])

categories = ['sport', 'politics', 'economics', 'culture', 'music', 'science', 'society', 'healthcare', 'weather']

dataset.id = np.arange(1, 100001)
dataset.set_index('id', inplace=True)

dataset.sex = rng.choice(['male', 'female'], 100000)

dataset.age = rng.triangular(15, 35, 95, 100000).astype(int)

dataset.os = rng.choice(os, p=[0.36, 0.07, 0.01, 0.35, 0.18, 0.03], size=100000)

r = requests.get('https://ru.wikipedia.org/wiki/Субъекты_Российской_Федерации')

soup = BeautifulSoup(r.text)

regions = []

for i in pd.Series(soup.find_all('table')[2].tbody.find_all('tr')).apply(lambda x: x.find_all('td'))[1::]:
    try:
        int(i[0].text)
    except:
        continue
    else:
        regions.append(i)

regions = pd.Series(regions).apply(lambda x: x[1].text)

regions = regions.str.replace('\[\d+\]', '', regex=True)

dataset.region = rng.choice(regions, 100000)

dataset.category_1 = rng.choice(categories, 100000)
dataset.category_2 = rng.choice(categories, 100000)
dataset.category_3 = rng.choice(categories, 100000)

dataset.mark_1 = rng.triangular(6, 9, 10, 100000)
dataset.mark_2 = rng.triangular(5, 8, 10, 100000)
dataset.mark_3 = rng.triangular(4, 7, 10, 100000)

print(dataset.head())
dataset.to_sql(name='customers', con=engine, if_exists='replace')
