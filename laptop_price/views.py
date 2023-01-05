import os
import pickle

import requests
from rest_framework.response import Response
from rest_framework.views import APIView
import numpy as np
from skstores.settings import BASE_DIR
from skstores.utils import download_file_from_azure_container

# Create your views here.

download_file_from_azure_container('laptop_price/final_df_laptop_price.pkl', 'laptop_price/files/laptop_price.pkl')
download_file_from_azure_container('laptop_price/final_pipe_gradient_boost.pkl', 'laptop_price/files/laptop_pipe.pkl')

laptop_df = pickle.load(open(f'{BASE_DIR}/laptop_price/files/laptop_price.pkl', 'rb'))
pipeline = pickle.load(open(f'{BASE_DIR}/laptop_price/files/laptop_pipe.pkl', 'rb'))


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
        # req_lpt = requests.get(gd_laptop_df)
        # print(req_lpt.content)
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
