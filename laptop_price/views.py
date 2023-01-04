import os
import pickle

from rest_framework.response import Response
from rest_framework.views import APIView
import numpy as np
from skstores.settings import BASE_DIR

# Create your views here.
# movie_file = open(os.path.join(settings.BASE_DIR, 'df_movie.pkl'))
laptop_df = pickle.load(open(f'{BASE_DIR}/laptop_price/files/final_df_laptop_price.pkl', 'rb'))
pipeline = pickle.load(open(f'{BASE_DIR}/laptop_price/files/final_pipe_gradient_boost.pkl', 'rb'))


# for index, row in movies_df.iterrows():
#     movie_list.append({'movie_index': index, 'id': row.id, 'title': row.title})
#     count += 1
#     # if count > 15:
#     #     break
# sorted_movie_list = sorted(list(movie_list), key=lambda x: x['title'])

# print(json.dumps(sorted_movie_list))


class LaptopFeatures(APIView):
    def get(self, request):
        column_values = []
        columns = laptop_df.columns
        # print(columns)
        for column in columns:
            col = ' '.join(column.split('_')).upper()
            if 'GNRTN' in col:
                col = 'PROCESSOR GEN'
            # print(list(set(laptop_df[column])))
            column_values.append({'column': col, 'value': list(set(laptop_df[column]))})
            # column_values.append({col: 'a'})
        #
        # print(column_values)
        return Response(column_values, 200)


class PredictPrice(APIView):
    def post(self, request):
        # print(request.data)
        laptop_features_to_predict = []
        for (index, column) in enumerate(request.data):
            # print(index, column)
            # print(request.data[column])
            laptop_features_to_predict.append(request.data[column])
        laptop = ['Lenevo', 'A6-9225', 'AMD', 'A6-9225 Processor', '10', '4', 'DDR4',
                  '0', '1024', 'Windows', '64', '0', 'ThinNlight', '15.12', '0', '0',
                  '0']
        price = np.exp(pipeline.predict(np.array(laptop_features_to_predict).reshape(1, 17))[0])
        # laptop_data = request.data.get('laptop_data')
        # price = pipeline.predict(laptop_data)
        return Response(round(price, 2), 200)
