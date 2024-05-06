from sklearn.cluster import KMeans
from numpy import histogram
from pandas.api.types import is_numeric_dtype
import database_operations


def description():
    return database_operations.get_db().describe().reset_index(names='metric').to_dict(orient='list')


def clustering(n_clusters, columns=None):
    table = database_operations.get_db(columns)
    kmeans = KMeans(n_clusters=n_clusters).fit(table)
    table['labels'] = kmeans.labels_
    result_table = table.sample(frac=0.1)
    result = {'x': result_table.iloc[:, 0].tolist(), 'y': result_table.iloc[:, 1].tolist(),
              'colors': result_table.labels.tolist()}
    return result


def hist(column):
    table = database_operations.get_db(column)
    if is_numeric_dtype(table[column[0]]):
        histog = histogram(table)
        names = []
        for i in range(1, len(histog[1])):
            names.append(str(histog[1][i - 1]) + "-" + str(histog[1][i]))
        return {'names': names, 'values': histog[0].tolist()}
    else:
        return {'names': table.value_counts().reset_index().iloc[:, 0].values.tolist(),
                'values': table.value_counts().reset_index().iloc[:, 1].values.tolist()}
