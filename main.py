from fastapi import FastAPI
import uvicorn
app=FastAPI()


# This file you will find all sessions of the tutorial.

# ============================ First Session ============================

# Instructions to run the server:
# 1. Install Uvicorn: Uvicorn is an ASGI server that is commonly used to run FastAPI applications. You can install it using pip:
# pip install uvicorn
# 2. Run the server: Use the following command to run the FastAPI application:
# uvicorn main:app --reload


# Flags:
# --port: Specifies the port number on which the server will listen for incoming requests. By default, FastAPI runs on port 8000, but you can change it to any available port.
# --reload: Automatically reloads the server when code changes are detected. This is useful during development to see changes without restarting the server manually.
# --host: Specifies the host address on which the server will listen. By default, FastAPI listens on localhost.
# Example: uvicorn main:app --reload --port 8080


@app.get("/") # --> this is called a decorator, it is used to define the route for the endpoint. In this case, it defines a GET request for the root URL ("/").
# question - what if i changed the route to "/hello"?
# Answer - If you change the route to "/hello", the endpoint will be accessible at http://localhost:8000/hello instead of http://localhost:8000/.


# question - why do we use get in the first place?
# Answer - We use GET to retrieve data from the server. It is one of the HTTP methods used to request data from a specified resource.
async def root():
    return {"message":"hello world"}


@app.post("/", deprecated=True) #--> this defines a POST request for the root URL ("/"). POST requests are typically used to submit data to the server, such as form data or JSON payloads.
async def post():
    return {"message":"This is a POST request"}


@app.put("/", description="Update an existing resource") #--> this defines a PUT request for the root URL ("/"). PUT requests are typically used to update existing resources on the server.
# question - what is a resource in this context?
# Answer - In this context, a resource refers to any data or object that can be accessed.
# in simple words, a resource is something that can be created, read, updated, or deleted on the server. It could be a user, a product, a blog post, etc.

# question - what is the difference between POST and PUT?
# Answer - The main difference between POST and PUT is that POST is used to create a new resource, while PUT is used to update an existing resource.
async def put():
    return {"message":"This is a PUT request"}

@app.delete("/") #--> this defines a DELETE request for the root URL ("/"). DELETE requests are typically used to delete resources from the server.
async def delete():
    return {"message":"This is a DELETE request"}


# ============================ Second Session ============================


# path parameters: These are variables that are part of the URL path. They are defined using curly braces {} in the route. For example, in the route "/items/{item_id}", "item_id" is a path parameter that can be accessed in the function as an argument.
@app.get("/movie_id/{movie_id}")
async def get_movie(movie_id: int): # --> : int is a type hint that indicates that the movie_id parameter should be of type integer. This helps FastAPI to validate the input and ensure that it receives the correct data type.
    return {"movie_id": movie_id}

# Note: always put static routes before dynamic routes. For example, if you have a route "/movies/{movie_id}" and another route "/movies/top", the static route "/movies/top" should be defined before the dynamic route "/movies/{movie_id}". This is because FastAPI matches routes in the order they are defined, and if the dynamic route is defined first, it will match all requests to "/movies/*", including "/movies/top".

from enum import Enum

class Genre(str, Enum):
    action = "action"
    comedy = "comedy"
    drama = "drama"

@app.get("/movies/genre/{genre}")
async def get_movies_by_genre(genre: Genre):
    return {"genre": genre}


@app.get("/admin", include_in_schema=False) #--> this defines a GET request for the "/admin" route, but it will not be included in the OpenAPI schema documentation. This means that it will not appear in the automatically generated API documentation, and it will not be accessible through the interactive API docs interface.
async def admin():
    return {"message": "This is the admin endpoint"}


# ============================ Third Session ============================

# make a list of movies with id,title,genre and rating
movies = [
    {"id": 1, "title": "The Shawshank Redemption", "genre": "drama", "rating": 9.3},
    {"id": 5, "title": "Forrest Gump", "genre": "comedy", "rating": 8.8},
    {"id": 3, "title": "The Dark Knight", "genre": "action", "rating": 9.0},
    {"id": 4, "title": "Pulp Fiction", "genre": "crime", "rating": 8.9},
    {"id": 2, "title": "The Godfather", "genre": "crime", "rating": 9.2},
    {"id": 7, "title": "The Matrix", "genre": "action", "rating": 8.7},
    {"id": 6, "title": "Inception", "genre": "action", "rating": 8.8},
    {"id": 10, "title": "The Green Mile", "genre": "drama", "rating": 8.6},
    {"id": 8, "title": "The Lord of the Rings: The Return of the King", "genre": "fantasy", "rating": 8.9},
    {"id": 9, "title": "The Silence of the Lambs", "genre": "thriller", "rating": 8.6}
]

@app.get("/movies")
async def get_movies(start: int=0, limit: int=10):
    return movies[start:start+limit]


@app.get("/movies/rating")
async def movies_by_rating(range: float = 8.8):
    sorted_movies = sorted(movies, key=lambda x: x["rating"], reverse=True)
    if range:
        sorted_movies=[movie for movie in sorted_movies if movie["rating"]>=range]
    return sorted_movies


# ============================ Fourth Session ============================

from pydantic import BaseModel

class MovieItem(BaseModel):
    id: int
    title: str
    genre: str
    rating: float
    description: str = None # --> this is an optional field, it can be left out when creating a new movie
    description2: str| None = None # --> this is another way to define an optional field using Union type hint
    up_votes: int = 0
    down_votes: int = 0

@app.post("/movies")
async def create_movie(movie: MovieItem):
    movie_dict = movie.dict() # --> this converts the Pydantic model instance into a dictionary, which can be easily manipulated and stored in the movies list.
    total_votes = movie_dict["up_votes"] + movie_dict["down_votes"]
    movie_dict.update({"total_votes": total_votes})
    return {"message": "Movie created successfully", "movie": movie_dict}


@app.put("/movies/{movie_id}")
async def update_movie(movie_id: int, movie: MovieItem):
    for m in movies:
        if m["id"] == movie_id:
            m.update(movie.dict())
            return {"message": "Movie updated successfully", "movie": m}
    return {"message": "Movie not found"}

# the main difference between POST and PUT is that POST is used to create a new resource, while PUT is used to update an existing resource.
# In the context of the above code, the POST endpoint is used to create a new movie, while the PUT endpoint is used to update an existing movie based on its ID.


# ============================= Fifth Session ============================

# in fifth session we will learn about how to use pickle to save and load data, and how to use it in our FastAPI application.
# We will also learn about the advantages of using pickle over json, and how to preserve the methods of a class when saving it to a file.

# go to the avoid/json_w_r.py file to see how to use json to save and load data,
# and then go to the prefered/pickle_thing.py file to see how to use pickle to save and load data.

# i trained a really basic logistic regression model on the iris dataset, and saved it to a pickle file in the simple_model/model.py file.
# You can go there to see how to do that, and then we will learn how to load that model in our FastAPI application and use it to make predictions.

# also created a visualization.ipynb file in the simple_model directory, where we will visualize the iris dataset using matplotlib.

# lets try this model out in the FastAPI application, we will create a new endpoint that takes in the features of the iris dataset and returns the predicted class.

class input_data(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

classes_names = ["setosa", "versicolor", "virginica"]
@app.post("/predict")
async def predict(input_features: input_data):
    import pickle
    import os

    # load the model from the pickle file
    with open(os.path.join("simple_model", "model_LR.pkl"), "rb") as f:
        model = pickle.load(f)

    # create a feature array from the input parameters
    features = [[input_features.sepal_length, input_features.sepal_width, input_features.petal_length, input_features.petal_width]]

    # make a prediction using the loaded model
    prediction = model.predict(features)

    return {"predicted_class": classes_names[prediction[0]]}

# example url to test the predict endpoint:
# http://localhost:8000/docs
# then click on the POST /predict endpoint, then click on "Try it out", you will be able to input the features of the iris dataset and see the predicted class.
