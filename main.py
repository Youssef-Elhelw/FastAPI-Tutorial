from email import message

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

# ============================= Sixth Session ============================

# in this session we will learn about Input validation using BaseModel and  Field from pydantic.
from pydantic import Field, field_validator

class MovieItemV2(BaseModel):
    id: int = Field(..., gt=0, description="The ID of the movie, must be a positive integer")
    title: str = Field(..., min_length=1, max_length=100, description="The title of the movie, must be between 1 and 100 characters")
    genre: str = Field(..., min_length=1, max_length=50, description="The genre of the movie, must be between 1 and 50 characters")
    rating: float = Field(..., ge=0.0, le=10.0, description="The rating of the movie, must be between 0.0 and 10.0")
    description: str = Field(None, max_length=500, description="The description of the movie, must be less than 500 characters")
    up_votes: int = Field(0, ge=0, description="The number of up votes for the movie, must be a non-negative integer")
    down_votes: int = Field(0, ge=0, description="The number of down votes for the movie, must be a non-negative integer")

    views:int
    @field_validator("views")
    def validate_views(cls, value):
        if value < 0:
            raise ValueError("Views must be a non-negative integer")
        return value

@app.post("/movies/v2")
async def create_movie_v2(movie: MovieItemV2):
    return {"message": "Movie created successfully", "movie":movie.model_dump()}


# ============================= Seventh Session ============================

# in this session we will learn about API security and authentication using FastAPI's built-in security utilities. We will implement basic authentication and token-based authentication to secure our API endpoints.
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

# first thing we should do is to create an API key header that will be used for authentication. We can use the APIKeyHeader class from fastapi.security to create this header.
api_key_header = APIKeyHeader(name="X-API-Key")

# next, we will create a function that will be used to verify the API key. This function will check if the API key provided in the header matches a predefined API key.
def verify_api_key(api_key: str = Depends(api_key_header)):
    predefined_api_key = "my_secret_api_key"
    if api_key != predefined_api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    else:
        return True
    
# let's test it
@app.get("/secure-data")
async def get_secure_data(api_key_valid: bool = Depends(verify_api_key)):
    return {"message": "This is secure data, you have access to it successfully!"}

# how to test it:
# 1. Open the interactive API docs at http://localhost:8000/docs
# 2. Find the GET /secure-data endpoint and click on it to expand the details.
# 3. Click on the "Try it out" button to enable the input fields.
# 4. you will see in the top right corner of the request body a lock icon, click on it to open the authentication dialog.
# 5. In the "X-API-Key" field, enter the predefined API key (in this case, "my_secret_api_key").
# 6. Click the "Execute" button to send the request.

# ============================= Eighth Session ============================

# let's dive into rate limiting and how to implement it in our FastAPI application.
# Rate limiting is a technique used to control the amount of incoming traffic to an API endpoint, which can help prevent abuse and ensure fair usage of resources.
# for example, we can limit the number of requests a user can make to a specific endpoint within a certain time frame (e.g., 10 requests per minute).
# if limit is exceeded, we can return a 429 Too Many Requests response to the user, indicating that they have exceeded the allowed number of requests and should try again later.

from datetime import datetime, timedelta


from collections import defaultdict
# this one is used to create a dictionary that will store the timestamps of the requests made by each user. 
# It allows us to easily manage and track the request history for each user without having to worry about handling missing keys or initializing lists for new users.



class RateLimiter:
    def __init__(self, requests_per_minute: int=10):
        self.requests_per_minute = requests_per_minute
        self.user_requests = defaultdict(list)
    
    def is_rate_limited (self,api_key:str) -> tuple[bool, int]: # the -> tuple[bool, int] is a type hint that indicates that the function will return a tuple containing a boolean value and an integer value.
        # The boolean value indicates whether the user is rate limited or not, and the integer value indicates the number of requests made by the user in the last minute.
        
        current_time = datetime.now()
        minute_ago = current_time - timedelta(minutes=1)
        # we will filter out the timestamps that are older than one minute from the current time, and then check if the number of remaining timestamps exceeds the allowed number of requests per minute.
        self.user_requests[api_key] = [timestamp for timestamp in self.user_requests[api_key] if timestamp > minute_ago] # this line filters out the timestamps that are older than one minute from the current time, and updates the user_requests dictionary to only keep the recent timestamps for each user.
        if len(self.user_requests[api_key]) >= self.requests_per_minute:
            return True, "Rate limit exceeded. Try again later."
        else:
            self.user_requests[api_key].append(current_time)
            return False, len(self.user_requests[api_key])
        
# now we can create an instance of our RateLimiter class.
rate_limiter = RateLimiter(requests_per_minute=10)

def test_rate_limit(api_key: str = Depends(api_key_header)):
    # check if the API key is authenticated
    if api_key != "my_secret_api_key":
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    # if so, check if the user exceeds the rate limit or not
    is_limited, note = rate_limiter.is_rate_limited(api_key)
    if is_limited:
        raise HTTPException(status_code=429, detail=note)
    else:
        return True
    

# now let us try this out in our pre-trained model endpoint, and for each request, we will notify the user about how many requests are remaining for them in the current minute.
# and when it will be reset, so they can know when to make the next request if they exceed the limit.
@app.post("/predict/v2")
async def predict_v2(input_features: input_data, api_key_valid: bool = Depends(test_rate_limit)):
    import pickle
    import os

    # load the model from the pickle file
    with open(os.path.join("simple_model", "model_LR.pkl"), "rb") as f:
        model = pickle.load(f)

    # create a feature array from the input parameters
    features = [[input_features.sepal_length, input_features.sepal_width, input_features.petal_length, input_features.petal_width]]

    # make a prediction using the loaded model
    prediction = model.predict(features)

    return {"predicted_class": classes_names[prediction[0]], "note": "You have made {} requests in the last minute. You can make {} more requests before the limit resets.".format(len(rate_limiter.user_requests["my_secret_api_key"]), rate_limiter.requests_per_minute - len(rate_limiter.user_requests["my_secret_api_key"]))}

# ============================= Ninth Session ============================

# in this session we will learn about how to use background tasks in FastAPI to perform time-consuming operations without blocking the main thread of the application.
# We will implement a simple background task that simulates a long-running process, and we will see how to use it in our API endpoints to improve the responsiveness of our application.


#  importing pre-trained model
from nltk.sentiment import SentimentIntensityAnalyzer
from fastapi import BackgroundTasks
import time

sia = SentimentIntensityAnalyzer()

def process_sentiment(text: str):
    # this function will be run in the background to process the sentiment of the input text
    sentiment_scores = sia.polarity_scores(text)
    print(f"Sentiment scores for '{text}': {sentiment_scores}")
    print("Final sentiment:", "Positive" if sentiment_scores["compound"] > 0 else "Negative" if sentiment_scores["compound"] < 0 else "Neutral")
    time.sleep(5) # simulating a long-running process


@app.post("/sentiment")
async def analyze_sentiment(text: str, background_tasks: BackgroundTasks):
    # this endpoint will receive a text input and will trigger the background task to process the sentiment of the text
    background_tasks.add_task(process_sentiment, text)
    return {"message": "Sentiment analysis is being processed in the background. You will see the results in the console shortly."}

# ============================= Tenth Session ============================

# in this this session we will know how to update versions of our API without breaking the existing clients that are using the old version. 
# We will implement versioning in our FastAPI application and see how to maintain backward compatibility while introducing new features and improvements in the newer versions of the API.

# Question: Why do we need API versioning?

# Answer: We need API versioning to introduce:

# 1. new features
# 2. performance improvements
# 3. bug fixes
# 4. updated ML models
# 5. improved training data
# 6. changed response formats

# without breaking applications that still use the older API version.
# Versioning allows old clients to continue working normally while giving new clients access to improved functionality.
# This is especially important in machine learning systems because model behavior and outputs may change over time.

# Question - When should we update the version of our API?

# Answer:

# 1. removing existing endpoints
# 2. renaming endpoints
# 3. changing request parameters
# 4. changing response structure
# 5. modifying prediction logic significantly
# 6. updating the ML model in a way that changes outputs
# 7. updating training data that affects recommendations or predictions

@app.get("/v1/movies")
async def get_movies_v1():
    return {"movies": movies}


@app.get("/v2/movies")
async def get_movies_v2():
    # in this version, we will return the movies sorted by rating in descending order
    sorted_movies = sorted(movies, key=lambda x: x["rating"], reverse=True)
    return {"movies": sorted_movies}

# Clients using /v1/movies will continue working without any issue, while newer clients can use /v2/movies for improved functionality.
# This is exactly the purpose of API versioning.


# Improtant note:
# If the change does not break compatibility (for example, adding an optional field), a new version may not be necessary.

# for example.

class movie_item(BaseModel):
    id: int
    title: str
    genre: str
    rating: float
    # if new field is added, it should be optional to avoid breaking existing clients
    date:str=None



# ============================= Final Session ============================

# in this session we will learn about
# Logging: We will learn how to implement logging in our FastAPI application to keep track of important events, errors, and other relevant information.
# This can help us monitor the health of our application and troubleshoot issues when they arise.

# Question: What is logging and why is it important in a FastAPI application?
# Answer: Logging is the process of recording events, errors, and other relevant information in an application. 

# It is important in a FastAPI application because it helps us monitor the health of our application, troubleshoot issues, 
# and gain insights into how users are interacting with our API.
#  
# By implementing logging, we can track important events such as incoming requests, responses, errors, and other relevant information 
# that can help us identify and resolve issues quickly.

# there are different logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) that we can use to categorize our log messages based on their severity and importance.

import logging

logger=logging.getLogger("uvicorn.error") # this will get the logger used by Uvicorn to log errors, so we can use it to log our own messages as well.

logger.info("App is running...") # this will log an informational message indicating that the application is running.

@app.get("/log-test")
async def log_test():
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    return {"message": "Check the logs for the logged messages."}


# a very important usage of logging is with Middleware, we can create a custom middleware to log all incoming requests and their responses, 
# which can help us monitor the traffic and identify any issues with specific endpoints or requests.

from fastapi import Request

# Question: What is Middleware in FastAPI?
# Answer: Middleware in FastAPI is a way to process requests and responses globally before they reach the endpoint functions.

# This is very useful in real projects because it helps you know:

# - which endpoint is slow
# - how much time each request needs
# - performance bottlenecks in your API

# Request -> Middleware -> Endpoint -> Middleware -> Response

# So middleware can:

# check authentication
# add headers
# measure execution time
# logging
# rate limiting

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info(f"Request processed in {process_time:.2f} seconds")
    return response

# Question: what is the call_next function in the middleware?
# Answer: The call_next function is a callable that takes a Request object as an argument and returns a Response object. 
# It is used to pass the request to the next middleware or endpoint in the processing chain. 
# When you call call_next(request), it will execute the next middleware or endpoint and return the response generated by that middleware or endpoint. 
# This allows you to perform actions before and after the request is processed, 
# such as logging the request and measuring the execution time, as shown in the log_requests middleware example above.