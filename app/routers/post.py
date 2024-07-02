from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..import models, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import Optional 


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]

)


# @router.get("/")
# def root():
#     return {"message": "Welcome to my API!! "}


@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int =10, skip: int =0, search: Optional[str]= "" ):

    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(
    #     models.Post.owner_id == current_user.id).all()
    # return posts
    print(limit)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()



    posts  = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
                                          isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    


    return posts

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int ,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):


    #post = db.query(models.Post).filter(models.Post.id == id).first()
    #print(post)


    post= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
                                          isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"post with id: {id} was not found")
    
       #the code below can make only the owner see it - restricted view 
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorised to perform request action ")
     
    #return {"post_detail" : post}
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
#@router.post("/")
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):

 
    print(current_user.id)
    print(current_user.email)
    new_post = models.Post( owner_id= current_user.id ,**post.dict())
    # new_post =  models.Post(
    #     title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_404_NOT_FOUND)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post =cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)


    post = post_query.first()

    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with the {id} does not exist")
    #the code below can make only the owner see it - restricted view 
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform request action ")
    

    post_query.delete(synchronize_session = False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#ISUESS with update post ! teh data base changes but return statement give "Internal server error"
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 

 post_query = db.query(models.Post).filter(models.Post.id == id)
 post = post_query.first()
 
 if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with the {id} does not exist")

 if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform request action ")
 post_query.update(updated_post.dict(), synchronize_session=False)
 db.commit()

 return post_query.first()