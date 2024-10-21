import numpy as np

'''
베스트 셀러 방식은 모든 사용자에게 각 영화의 평균 평점을 예측값으로 사용하는 추천 시스템 방식 
복잡한 사용자 맞춤형 알고리즘 없이 영화 자체의 평점에 기반함
'''

# 모델의 예측값이 실제 데이터와 얼마나 차이가 있는지, 즉 예측 성능을 수치화 해주는 메서드 RMSE가 낮을수록 실제 데이터와 가깝다
def RMSE(y_true, y_pred):
  return np.sqrt(np.mean((np.array(y_true) - np.array(y_pred))**2))


#정확도 계산

rmse = [] #rms값 집어넣을 배열
movie_mean = ratings.groupby(['movie_id'])['rating'].mean() #무비들의 각 평점의 평균값을 계산

for user in set(ratings.index):
  y_true = ratings.loc[user]['rating'] #현재 유저가 평가한 영화들의 실제 평점 리스트
  '''
  예를 들어, 만약 사용자가 user_1이라고 하고 그 사용자가 세 개의 영화에 대해 평점을 매겼다면, y_true에는 그 세 개의 영화에 대한 실제 평점들이 들어감
	•	예시: 사용자가 Movie A에 4점, Movie B에 5점, Movie C에 3점을 줬다면 y_true = [4, 5, 3]이 됨
  '''

  # 해당 유저가 평점을 남긴 영화들의 best-seller 방식으로 추출된 예측 점수값을 뽑아와서 리스트로 만듦
  y_pred = movie_mean[ratings.loc[user]['movie_id']]

  '''
  사용자가 Movie A, Movie B, Movie C에 대해 평점을 매겼다면 movie_id는 [A, B, C]가 될 거야.
	•	movie_mean[ratings.loc[user]['movie_id']]: 이 코드는 해당 영화들의 평균 평점을 가져와. 각 영화의 평균 평점이 **예측된 평점(y_pred)**이 되는 거지.
	•	예시: Movie A의 평균 평점이 4.2점, Movie B의 평균 평점이 4.8점, Movie C의 평균 평점이 3.5점이라면 y_pred = [4.2, 4.8, 3.5]이 되는 거야.
  '''

  '''
  •	y_true: 사용자가 실제로 영화에 매긴 평점. 예: [4, 5, 3]
	•	y_pred: Best-Seller 방식으로 계산한 영화의 평균 평점. 예: [4.2, 4.8, 3.5]
  '''

  accuracy = RMSE(y_true, y_pred)
  rmse.append(accuracy)

# RMSE 계산
print(np.mean(rmse))