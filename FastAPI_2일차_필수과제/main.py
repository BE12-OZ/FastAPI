from fastapi import FastAPI, status, Path, HTTPException, Response
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

# Pydantic 모델 정의
class Movie(BaseModel):
    title: str
    playtime: int
    genre: str

class MovieUpdate(BaseModel):
    title: str
    playtime: int = Field(..., gt=0, description="재생 시간은 0보다 커야 합니다.")
    genre: str

class MovieDB(Movie):
    id: int

# 인메모리 데이터베이스
movie_db = []
movie_id_counter = 0

@app.post("/movies", response_model=MovieDB, status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie):
    """
    새로운 영화 정보를 받아 등록하고, 등록된 영화 정보를 반환합니다.
    """
    global movie_id_counter
    movie_id_counter += 1
    
    new_movie = MovieDB(
        id=movie_id_counter,
        title=movie.title,
        playtime=movie.playtime,
        genre=movie.genre
    )
    movie_db.append(new_movie)
    return new_movie

@app.get("/movies", response_model=List[MovieDB])
def get_movies(title: Optional[str] = None, genre: Optional[str] = None):
    """
    쿼리 파라미터로 영화를 검색하고, 조건에 맞지 않으면 전체 목록을 반환함.
    """
    result = movie_db
    
    # 검색 조건이 있는 경우
    if title or genre:
        filtered_movies = result
        if title:
            filtered_movies = [m for m in filtered_movies if title.lower() in m.title.lower()]
        if genre:
            filtered_movies = [m for m in filtered_movies if genre.lower() in m.genre.lower()]
        
        # 검색 결과가 있으면 해당 결과 반환, 없으면 전체 목록 반환
        if filtered_movies:
            return filtered_movies
        else:
            return result
    
    # 검색 조건이 없는 경우 전체 목록 반환
    return result

@app.get("/movies/{movie_id}", response_model=MovieDB)
def get_movie_by_id(movie_id: int = Path(..., gt=0, description="조회할 영화의 ID")):
    """
    경로 파라미터로 전달된 ID를 사용하여 영화 정보를 조회함.
    """
    for movie in movie_db:
        if movie.id == movie_id:
            return movie
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 ID의 영화를 찾을 수 없습니다.")

@app.put("/movies/{movie_id}", response_model=MovieDB)
def update_movie(movie_update: MovieUpdate, movie_id: int = Path(..., gt=0, description="수정할 영화의 ID")):
    """
    경로 파라미터로 전달된 ID를 사용하여 영화 정보를 수정.
    """
    for i, movie in enumerate(movie_db):
        if movie.id == movie_id:
            updated_movie = MovieDB(
                id=movie_id,
                title=movie_update.title,
                playtime=movie_update.playtime,
                genre=movie_update.genre
            )
            movie_db[i] = updated_movie
            return updated_movie
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 ID의 영화를 찾을 수 없습니다.")

@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int = Path(..., gt=0, description="삭제할 영화의 ID")):
    """
    경로 파라미터로 전달된 ID를 사용하여 영화 정보를 삭제.
    """
    movie_to_delete = None
    for movie in movie_db:
        if movie.id == movie_id:
            movie_to_delete = movie
            break
    
    if movie_to_delete:
        from fastapi import FastAPI, status, Path, HTTPException, Response, Header, Cookie
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

# --- Pydantic 모델 정의 ---

class Movie(BaseModel):
    # 2. Field를 이용한 검증 강화
    title: str = Field(..., min_length=1, description="영화 제목")
    playtime: int = Field(..., gt=0, description="재생 시간 (분)")
    genre: str = Field(..., min_length=2, description="영화 장르")

    # 4. Swagger 문서에 요청 예제 표시
    class Config:
        schema_extra = {
            "example": {
                "title": "어벤져스: 엔드게임",
                "playtime": 181,
                "genre": "액션",
            }
        }

class MovieUpdate(BaseModel):
    title: str = Field(..., min_length=1, description="영화 제목")
    playtime: int = Field(..., gt=0, description="재생 시간은 0보다 커야 합니다.")
    genre: str = Field(..., min_length=2, description="영화 장르")

class MovieDB(Movie):
    id: int

# --- 인메모리 데이터베이스 ---
movie_db = []
movie_id_counter = 0

# --- API 엔드포인트 ---

@app.post("/movies", response_model=MovieDB, status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie):
    """
    새로운 영화 정보를 받아 등록하고, 등록된 영화 정보를 반환함.
    """
    global movie_id_counter
    movie_id_counter += 1
    
    new_movie = MovieDB(
        id=movie_id_counter,
        **movie.dict()
    )
    movie_db.append(new_movie)
    return new_movie

@app.get("/movies", response_model=List[MovieDB])
def get_movies(
    title: Optional[str] = None,
    genre: Optional[str] = None,
    # 5. 헤더 및 쿠키 파라미터
    user_agent: Optional[str] = Header(None, description="사용자 브라우저 정보"),
    session_id: Optional[str] = Cookie(None, description="사용자 세션 ID")
):
    """
    쿼리 파라미터로 영화를 검색하고, 조건에 맞지 않으면 전체 목록을 반환.
    - **Header**와 **Cookie** 값을 받아 터미널에 출력해줌.
    """
    print(f"Request from User-Agent: {user_agent}")
    print(f"User Session ID: {session_id}")

    result = movie_db
    
    if title or genre:
        filtered_movies = result
        if title:
            filtered_movies = [m for m in filtered_movies if title.lower() in m.title.lower()]
        if genre:
            filtered_movies = [m for m in filtered_movies if genre.lower() in m.genre.lower()]
        
        if filtered_movies:
            return filtered_movies
        else:
            return result
    
    return result

@app.get("/movies/{movie_id}", response_model=MovieDB)
def get_movie_by_id(movie_id: int = Path(..., gt=0, description="조회할 영화의 ID")):
    """
    경로 파라미터로 전달된 ID를 사용하여 영화 정보를 조회.
    """
    for movie in movie_db:
        if movie.id == movie_id:
            return movie
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 ID의 영화를 찾을 수 없습니다.")

@app.put("/movies/{movie_id}", response_model=MovieDB)
def update_movie(movie_update: MovieUpdate, movie_id: int = Path(..., gt=0, description="수정할 영화의 ID")):
    """
    경로 파라미터로 전달된 ID를 사용하여 영화 정보를 수정.
    """
    for i, movie in enumerate(movie_db):
        if movie.id == movie_id:
            updated_movie = MovieDB(
                id=movie_id,
                **movie_update.dict()
            )
            movie_db[i] = updated_movie
            return updated_movie
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 ID의 영화를 찾을 수 없습니다.")

@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int = Path(..., gt=0, description="삭제할 영화의 ID")):
    """
    경로 파라미터로 전달된 ID를 사용하여 영화 정보를 삭제.
    """
    movie_to_delete = None
    for movie in movie_db:
        if movie.id == movie_id:
            movie_to_delete = movie
            break
    
    if movie_to_delete:
        movie_db.remove(movie_to_delete)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 ID의 영화를 찾을 수 없습니다.")

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 ID의 영화를 찾을 수 없습니다.")