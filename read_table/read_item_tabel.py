# u.item 파일을 DataFrame으로 읽기

u_item_src = os.path.join(base_src, 'u.item')

i_cols = ['movie_id','title','release date','video release date',
'IMDB URL','unknown','Action','Adventure','Animat ion', 'Children\'s','Comedy','Crime','Documentary ','Drama','Fantasy',
'Film- Noir','Horror','Musical','Mystery','Romance ','Sci-Fi','Thriller','War','Western']

movies = pd.read_csv(u_item_src, 
      sep = '|',
            names = i_cols,
            encoding = 'latin-1')
movies = movies.set_index('movie_id')
movies.head()
      