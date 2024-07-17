from fastapi import FastAPI, Response, status, HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db
from .. import models,schemas,oauth2
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
                   )

#Getting All Posts
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user), limit: int = 10,skip: Optional[int] = 0,
              search: Optional[str] =""):
    # def root():
        # cursor.execute(""" SELECT * FROM posts """)
        # posts = cursor.fetchall()
    print(limit)
    posts = db.query(models.Post)
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return results

#Create a Post
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                 (post.title,post.content, post.Published))
    # new_post = cursor.fetchone()
    # conn.commit()
     #model_dump serves the same purpose as dict, allowing you to convert your Pydantic model instances to dictionaries,
     # but it's the preferred method moving forward. Reason for line on dict
    new_post = models.Post(**post.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

#Getting a post
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: str, response = Response, db:Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(id,))
    # post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} was not found")
        # response.status_code =status.HTTP_404_NOT_FOUND
        # return {'message': f"Post with {id} was not found"}status.HTTP_404_NOT_FOUND
    
    return post

#Delete a Post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:str, db:Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",id)
    # post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    # conn.commit()
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Updating a post
@router.put("/{id}",response_model=schemas.Post)
def update_post(id: str, updated_post: schemas.PostCreate, db:Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title,post.content,post.Published,id))
    # update_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    # conn.commit()
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="Not authorized to perform requested action")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()

    return post_query.first()