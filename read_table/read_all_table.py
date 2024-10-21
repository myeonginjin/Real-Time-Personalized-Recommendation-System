import os
import pandas as pd

base_src = 'drive/MyDrive/RecoSys/Data'

#유저 테이블
u_user_src = os.path.join(base_src, 'u.user')
u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv(u_user_src,
                    sep = '|',
                    names = u_cols,
                    encoding = 'latin-1'
                    )

#아이템 테이블
u_item_src = os.path.join(base_src, 'u.item')
i_cols = ['movie_id','title','release date','video release date',
'IMDB URL','unknown','Action','Adventure','Animat ion', 'Children\'s','Comedy','Crime','Documentary ','Drama','Fantasy',
'Film- Noir','Horror','Musical','Mystery','Romance ','Sci-Fi','Thriller','War','Western']
movies = pd.read_csv(u_item_src, 
      sep = '|',
            names = i_cols,
            encoding = 'latin-1')

#평가 테이블
u_data_src = os.path.join(base_src, 'u.data')
r_cols = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_csv(u_data_src, 
      sep = '\t',
            names = r_cols,
            encoding = 'latin-1')

# ratings DataFrame에서 timestamp 제거
ratings = ratings.drop('timestamp' , axis =1)
movies = movies[['movie_id', 'title']]
