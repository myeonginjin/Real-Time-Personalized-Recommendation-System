import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

base_src = 'drive/MyDrive/RecoSys/Data'

#유저 테이블
u_user_src = os.path.join(base_src, 'u.user')
u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv(u_user_src,
                    sep = '|',
                    names = u_cols,
                    encoding = 'latin-1'
                    )
users = users.set_index('user_id')

#아이템 테이블
u_item_src = os.path.join(base_src, 'u.item')
i_cols = ['movie_id','title','release date','video release date',
'IMDB URL','unknown','Action','Adventure','Animat ion', 'Children\'s','Comedy','Crime','Documentary ','Drama','Fantasy',
'Film- Noir','Horror','Musical','Mystery','Romance ','Sci-Fi','Thriller','War','Western']
movies = pd.read_csv(u_item_src, 
      sep = '|',
            names = i_cols,
            encoding = 'latin-1')
movies = movies.set_index('movie_id')

#평가 테이블
u_data_src = os.path.join(base_src, 'u.data')
r_cols = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_csv(u_data_src, 
      sep = '\t',
            names = r_cols,
            encoding = 'latin-1')


# 정확도 (RMSE)를 계산하는 함수
def RMSE(y_true, y_pred) :
  return np.sqrt(np.mean((np.array(y_true) - np.array(y_pred))**2))


# 모델별 RMSE를 계산하는 함수
# 유사 집단의 크기를 미리 정하기 위해서 기존 score 함수에 neighbor_size 인자값 추가
def score(model, neighbor_size = 0) :
  # 테스트 데이터의 user_id와 movie_id 간 pair를 맞춰 튜플형 원소 리스트데이터 만듦
  id_paris = zip(x_test['user_id'], x_test['movie_id'])
  # 모든 사용자-영화 짝에 대해서 주어진 예측모델에 의해 예측값 계산 및 리스트형 데이터 생성
  y_pred = np.array([model(user,movie) for (user, movie) in id_paris])
  # 실제 평점값 
  y_true = np.array(x_test['rating'])
  return RMSE(y_true, y_pred)


##### 데이터 셋 만들기 #####
x = ratings.copy() # 원본 데이터 백업 용
y = ratings['user_id']

x_train, x_test, y_train, y_test = train_test_split(x,y,
                                                    test_size=0.25, # X와 Y데이터가 있는데, 이 데이터를 0.25사이즈로 나누겠다는 말. 즉, 스트레인 데이터가 전체 데이터에서 75%를 차지하고 나머지 25%를 테스트 셋으로 분리
                                                    stratify=y) # 계층화 추출, 원래 원천 테이터에 있는 y환경을 최대한 따라가고자 설정


rating_matrix = x_train.pivot(index = 'user_id', columns = 'movie_id', values = 'rating')


# 코사인 유사도 계산 #
# trian set의 모든 가능한 사용자 pair의 cosine similarities 계산 #
# 코사인 유사도를 계산하는 사이킷런의 라이브러리 
from sklearn.metrics.pairwise import cosine_similarity
# 코사인 유사도를 구하기 위해 rating 값을 복사하고, 계산 시 NaN값의 에러 대비를 위해 결축치를 0으로 대체
matrix_dummy = ratings_matrix.copy().fillna(0)
# 모든 사용자간 코사인 유사도 구함
user_similarity = cosine_similarity(matrix_dummy, matrix_dummy) # 코사인 방식 사용
# 필요한 값 조회를 위해 인덱스 및 컬럼명 지정
user_similarity = pd.DataFrame(user_similarity,
                               index=ratings_matrix.index,
                               columns=ratings_matrix.index)

# 유저간의 유사성 테이블 확인
#user_similarity   

''' 기본적인 CF 알고리즘 방식 
### 주어진 영화의 (movie_id) 가중평균 rating을 계산하는 함수 ###
def CF_simple(user_id, movie_id):
  if movie_id in ratings_matrix.columns:
    sim_scores = user_similarity[user_id].copy() #원본 훼손 방지 용
    movie_ratings = ratings_matrix[movie_id].copy()
    none_rating_idx = movie_ratings[movie_ratings.isnull()].index
    movie_ratings = movie_ratings.dropna()
    sim_scores = sim_scores.drop(none_rating_idx)
    mean_rating = np.dot(sim_scores, movie_ratings) / sim_scores.sum()
  else:
    mean_rating = 3.0

  return mean_rating
'''

def CF_knn(user_id, movie_id, neighbor_size = 0) :
  if movie_id in rating_matrix.columns:
    sim_scores = user_similarity[user_id].copy()
    movie_ratings = rating_matrix[movie_id].copy()
    none_rating_idx = movie_ratings[movie_ratings.isnull()].index
    movie_ratings = movie_ratings.dropna()
    sim_scores = sim_scores.drop(none_rating_idx)

    if neighbor_size == 0:  # 기본 협업 필터링 방식과 동일하게 적용
      mean_rating = np.dot(sim_scores, movie_ratings) / sim_scores.sum()

    else:
      if len(sim_scores) > 1 :  # 이웃 고려 협업 필터링 
        neighbor_size = min(neighbor_size, len(sim_scores)) # sim_socres가 보다 neighbor_size보다 작은 경우를 고려
        sim_scores = np.arrays(movie_ratings)
        user_idx = np.argsort(sim_scores) # sim_scores를 오름차순으로 idx를 뽑아냄 
        sim_scores = sim_scores[user_idx][-neighbor_size:] # neighbor_size 범위만큼 뒤에서 부터 긁어옴 
        movie_rating = np.dot(sim_scores[user_idx])[-neighbor_size:]
        mean_ratings = np.dot(sim_scores, movie_ratings) / sim_scores.sum()
      else : # sim_scores = sim_scores.drop(none_rating_idx) 여기서 다 떨궈져서 나만 남음 
        mean_rating = 3.0
  else : # movie_id가 rating train pivot table에 포함되지 않는 경우 고려
    mean_rating = 3.0
  
  return mean_rating


### CF를 고려한 협업 필터링 정확도 계산 ###
score(CF_knn, neighbor_size = 30)
