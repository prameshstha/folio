import os
import pickle

import requests
from django.core.files import File
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from skstores.settings import BASE_DIR
from skstores.utils import download_file_from_azure_container

# Create your views here.

download_file_from_azure_container('movie_recommend/df_movie.pkl', 'movie_recommendor/files/df_movie.pkl')
download_file_from_azure_container('movie_recommend/vector_similarity.pkl', 'movie_recommendor/files/vector_similarity.pkl')

movies_df = pickle.load(open(f'{BASE_DIR}/movie_recommendor/files/df_movie.pkl', 'rb'))
movies_vector_similarity = pickle.load(open(f'{BASE_DIR}/movie_recommendor/files/vector_similarity.pkl', 'rb'))
print(File(movies_df))

movies_df.drop(columns=['tags'], inplace=True)
movie_list = []
count = 0
for index, row in movies_df.iterrows():
    movie_list.append({'movie_index': index, 'id': row.id, 'title': row.title})
    count += 1
    # if count > 15:
    #     break
sorted_movie_list = sorted(list(movie_list), key=lambda x: x['title'])

# print(json.dumps(sorted_movie_list))


class Movie(APIView):
    def get(self, request):
        return Response(sorted_movie_list, 200)


class RecommendedMovie(APIView):
    def post(self, request):
        # print(request.data)
        movie_index = request.data.get('movie_index')
        top_five = sorted(list(enumerate(movies_vector_similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:11]
        # print(top_five)
        recommended_five = []
        for i in top_five:
            # print(movies_df.iloc[i[0]].title)
            # print(movies_df.iloc[i[0]])
            # recommended_five.append({'id': movies_df.iloc[i[0]].id, 'title': movies_df.iloc[i[0]].title})
            single_movie = json.loads(requests.get(f'https://api.themoviedb.org/3/movie/{movies_df.iloc[i[0]].id}?api_key=b105fd2105b38ae32e9df54f88014765').content)
            recommended_five.append({'similarity': round((i[1]*100), 2), 'single_movie': single_movie})
        return Response(recommended_five, 200)
