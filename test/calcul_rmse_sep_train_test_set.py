import os
import pandas as pd

from sklearn.model_selection import train_test_split  # 데이터셋을 트레인 셋과 테스트셋으로 분리햐주는 일반적인 테스트 분리 라이브러리


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

# 데이터 train, test set 분리


'''
모델이 학습할 데이터를 훈련 세트(training set), 모델의 성능을 테스트하기 위해 사용할 데이터를 테스트 세트(test set). 
또한 모델이 실전에서 보이는 성능을 일반화 성능(generalization performance)라고 함
'''

x = ratings.copy() #원본 데이터 복원 용
y = ratings['user_id']

x_train, x_test, y_train, y_test = train_test_split(x,y,
                                                    test_size=0.25, # X와 Y데이터가 있는데, 이 데이터를 0.25사이즈로 나누겠다는 말. 즉, 스트레인 데이터가 전체 데이터에서 75%를 차지하고 나머지 25%를 테스트 셋으로 분리
                                                    stratify=y) # 계층화 추출, 원래 원천 테이터에 있는 y환경을 최대한 따라가고자 설정

# 정확도 (RMSE)를 계산하는 함수
def RMSE(y_true, y_pred) :
  return np.sqrt(np.mean((np.array(y_true) - np.array(y_pred))**2))


# 모델별 RMSE를 계산하는 함수
def score(model) :
  id_paris = zip(x_test['user_id'], x_test['movie_id'])
  y_pred = np.array([model(user,movie) for (user, movie) in id_paris])
  y_true = np.array(x_test['rating'])
  return RMSE(y_true, y_pred)


# best_seller 함수를 이용한 정확도 계산
train_mean = x_train.groupby(['movie_id'])['rating'].mean()

def best_seller(user_id, movie_id):
  try :
    rating = train_mean[movie_id]

  except:
    rating = 3.0

  return rating

#score(best_seller)


# 성별에 따른 예측값 계산
# x_train과 users 데이터를 병합하여 사용자 정보(성별 등)를 포함한 평점 데이터셋 생성
merged_ratings = pd.merge(x_train, users)

# 사용자 정보 테이블(users)의 인덱스를 user_id로 설정
users = users.set_index('user_id')

# 영화별, 성별로 평점 평균 계산
# 각 영화(movie_id)와 성별(sex) 그룹에 대한 평점(rating)의 평균을 계산해 g_mean에 저장
g_mean = merged_ratings[['movie_id', 'sex', 'rating']].groupby(['movie_id', 'sex'])['rating'].mean()

'''
# g_mean  확인용
'''

# 영화 평점 매트릭스 생성 (사용자별로 영화에 매긴 평점을 행렬 형태로 변환)
# 각 사용자를 행으로, 각 영화를 열로 하고, 평점을 값으로 가지는 피벗 테이블 생성
rating_matrix = x_train.pivot_table(index='user_id',  # 행을 user_id로 설정
                                    columns='movie_id',  # 열을 movie_id로 설정
                                    values='rating')  # 값을 rating으로 설정

'''
# rating_matrix  확인용
'''

# 성별 기반 추천 시스템 함수 정의
def cf_gender(user_id, movie_id):
    # rating_matrix에 movie_id가 존재할 경우에만 처리
    if movie_id in rating_matrix.columns:
        # 사용자의 성별을 가져옴
        gender = users.loc[user_id]['sex']
        # 영화에 대해 해당 성별의 평균 평점이 있을 경우 해당 값을 사용
        if gender in g_mean[movie_id].index:
            gender_rating = g_mean[movie_id][gender]
        # 성별 평점 정보가 없을 경우 기본값(3.0) 사용
        else:
            gender_rating = 3.0
    # 해당 영화에 대한 정보가 없을 경우 기본값(3.0) 사용
    else:
        gender_rating = 3.0
    return gender_rating

# 성별 기반 추천 시스템의 RMSE 계산
score(cf_gender)

