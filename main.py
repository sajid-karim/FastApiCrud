"""
Basic CRUD APIs using FastAPI

"""

from typing import Optional
from fastapi import FastAPI, Response, responses, status, HTTPException
from pydantic import BaseModel
from random import randrange



app = FastAPI()

# posts storage
my_posts = [{
    'title': 'title of post 1',
    'content': 'content of post 1',
    'id': 1
}, {
    'title': 'Favorivate Foods',
    'content': 'Pizza, chicken breast, tikka',
    'id': 2
}]

# find post
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

# delete post
def post_delete(id):
    i = 0
    for p in my_posts:
        if p['id'] == id:
            my_posts.pop(i)
            return True
        i += 1
    return False
# update post
def post_update(post, id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            print("if")
            my_posts[i] = post
            post['id'] = id
            return True
    return False

# this field are required
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default value if user not provides a value
    rating: Optional[int] = None


@app.get('/')
def root():
    return {'message': 'Welcome to the API...'}


@app.get('/posts')
def get_posts():
    return {'data': my_posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    my_posts.append(post)
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {'data': post_dict}  # return new_post

@app.get("/posts/{id}") # path parameter -> id
def get_post(id: int, response: Response):
    post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"post with {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"post with {id} not found"}
    return {'post_details':post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    check = post_delete(id)
    if check:
        # print(my_posts)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        # print(my_posts)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    post = post.dict()
    check = post_update(post, id)
    if check:
        return {"message":post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")