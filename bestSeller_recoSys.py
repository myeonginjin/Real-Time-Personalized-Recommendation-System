# 인기 제품 방식 추천 시스템

def recom_movie(n_items):  
  movie_mean = ratings.groupby(['movie_id'])['rating'].mean() #rating에 대해서 movie_id 기준으로 전부 다 평균을 내줌
  movie_sort = movie_mean.sort_values(ascending=False)[:n_items] #위 값에 대해서 sorting을 진행했음. 평균값이 큰것대로 n_items개수만큼만
  recom_movie = movies.loc[movie_sort.index] #솔팅된 리스트에서 기존 테이블에서의 index를 뽑아냄. 이름을 알아내기 위해서.
  recomendations = recom_movie['title']
  return recomendations


recom_movie(5) #5개 베스트 셀러 추천