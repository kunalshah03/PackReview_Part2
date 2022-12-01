import os
import sys

sys.path.append(os.getcwd()[:-5]+"app")
from app import app 

def test_index_route():
    response = app.test_client().get('/')
    assert response.status_code == 200

def test_page_content_route():
    response = app.test_client().post('/pageContentPost',data={"search":"Setup"})
    assert response.status_code == 200

def test_add_post_route():
    response = app.test_client().post('/pageContentPost',data=
    {"job_title":"1",
    "job_description":"2",
    "department":"3",
    "locations":"4",
    "hourly_pay":"5",
    "benefits":"6",
    "review":"7",
    "rating":"2",
    "recommendation":"2",
    })
    assert response.status_code == 200

def test_add_review_route():
    response = app.test_client().get('/review')
    assert response.status_code == 200
    

def test_review_route():
    response = app.test_client().get('/pageContent')
    assert response.status_code == 200

test_index_route()
test_review_route()
test_add_review_route()
test_add_post_route()
test_page_content_route()
