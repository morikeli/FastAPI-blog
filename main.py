from fastapi import FastAPI, Depends, status, Response, HTTPException
from db.database import engine, SessionLocal
from sqlalchemy.orm import Session
from db.models import Blog
from typing import List
from db import schema
from db import models


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(request: schema.Blog, db: Session = Depends(get_db)):
    new_blog = Blog(
        title=request.title,
        body=request.body
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


# GET: get all blogs
@app.get('/blogs', response_model=List[schema.ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


# GET: get a blog using its ID.
@app.get('/blog/{id}', status_code=200, response_model=schema.ShowBlog)
def get_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(Blog.id == id).first()

    if blog is None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': 'Blog not found!'}

        # use HTTPException instead of the code block above.
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Blog not found!')

    return blog


# PUT: update a blog
@app.put('/blog/{id}/edit', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schema.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Blog not found!')
    
    blog.update(request)
    db.commit()

    return 'updated successfully!'


# DELETE: delete a blog
@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Blog not found!')
    
    blog.delete(synchronize_session=False)
    db.commit()

    return "Blog deleted successfully!"

