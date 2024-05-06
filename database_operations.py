import sqlalchemy
from sklearn.preprocessing import LabelEncoder
from pandas import read_sql_table
from pathlib import Path
from json import dump


def get_db(columns=None):
    engine = sqlalchemy.create_engine("postgresql://postgres:123@localhost:5432/postgres")
    table = read_sql_table('customers', engine, index_col='id', columns=columns)
    return table

def save_to_memory(data: dict):
    name = data.pop('Наименование')
    path = Path("./variants")
    path.mkdir(exist_ok=True)
    path = path.joinpath(f"{name}.json")
    with open(path, "w+") as file:
        dump(data, file)


def delete(name):
    path = Path("./variants").joinpath(f"{name}.json")
    path.unlink()
