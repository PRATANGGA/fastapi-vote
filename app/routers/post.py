from fastapi import FastAPI, Response ,status,HTTPException,Depends, APIRouter
from sqlalchemy import func
from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional, List

router = APIRouter(tags=["Posts"],prefix="/posts")

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)

    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    # posts = db.execute(
    #     'select posts.*, COUNT(votes.post_id) as votes from posts LEFT JOIN votes ON posts.id=votes.post_id  group by posts.id')
    # results = []
    # for post in posts:
    #     results.append(dict(post))
    # print(results)
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
# def create_post(payload: dict = Body(...)):
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db) ,current_user: int = Depends(oauth2.get_current_user)):
    # print(post) 
    # print(post.dict())
    # post_dict = post.dict()
    # post_dict["id"] = randrange(0,10000000)
    # my_posts.append(post_dict)
    # cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING * """, 
    #                (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # print(new_post)
    # conn.commit()
    # new_posts = models.Post(title=post.title,content=post.content,published=post.published)
    
    print(current_user.email)
    print(post.dict())
    new_posts = models.Post(owner_id=current_user.id,**post.dict())
    print(new_posts)
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts


@router.get("/{id}",response_model=schemas.PostOut)
def get_posts(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post =  db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).first()
    print(post)
    if not post : 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND ,detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'message': f"post with id: {id} was not found"}
        
    print(current_user.id)
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)
      # deleting post 
      # find the index in the array that required ID
      # my_posts.pop
    #   index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    print(current_user.id)
    post = post_query.first()
    if post == None : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    # my_posts.pop(index) 
    return Response(status_code=status.HTTP_204_NO_CONTENT)
      
      
@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int,updated_post: schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" Update posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,(post.title,post.content,post.published,str(id),))
    # # index = find_index_post(id)
    # update_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    post_query.update(updated_post.dict(),synchronize_session=False)
    
    db.commit()
      
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    return post_query.first()