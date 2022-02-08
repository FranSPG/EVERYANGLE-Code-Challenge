# EVERYANGLE-Code-Challenge
This is a code challenge for a position as a Senior Machine Learning Engineer at EVERYANGLE.

# How to reproduce the solution

## First step 
#### Clone the repo, you can download the code from [this url](https://github.com/FranSPG/EVERYANGLE-Code-Challenge/archive/refs/heads/main.zip) or, if you have git installed on your device, you can clone the repo using the following command line
```
git clone git@github.com:FranSPG/EVERYANGLE-Code-Challenge.git
```
#### You'll get something like this, if everything is ok.
![git_clone](images/git_cone.png)

## Second step
#### Next, you need to build the Docker images. If you want, you could run the process without Docker.
#### To start the process, use the following command line
```
docker-compose build
```
#### Once it finishes, you will see an output like this
![](images/docker_compose_build.png)

## Third step
#### In the third step, you need to sent the command line
```
docker-compose up
```
#### The output will be something like this
![](images/docker_compose_up.png)

## If we've been lucky, everything is ready and running.

### Now, you can go to [http://0.0.0.0:8000/](http://0.0.0.0:8000/) and interact with the software.

### The first view will be as following. Where you can go to a Swagger where you have the endpoints (This is not working properly). 
### You can also take a look at the Redocs, this is a documentation generated by the comments in the code, a feature of FastAPI, the framework that I've chosen to develop the solution.
### Finally, you have the Account button, where you can signup, login or logout.
![](images/first_screen.png)

### The Signup process is quite easy, you only need a Name, an Email and a Password.
![](images/sign_up_screen.png)

### I'll leave you the others endpoints to play around.

## To persist the data, I used [PostgreSQL](https://www.postgresql.org/), the [SQLAlchemy ORM](https://www.sqlalchemy.org/) and [Alembic](https://alembic.sqlalchemy.org/en/latest/) as a migration tool
### You can access to the database using the following command line
```
psql postgresql://fran:fran@localhost/media_library
```
The credentials, users, databases are hardcoded. I runned out of time and I thought that maybe other functionalities where more important to finish.

Sadly, I couldn't finish the tests. They worked when I had only the back-end but broke up when I added the templates and changed the requests and responses.


# Required Techniques

## Array or List
On the script [media_library/media_library/media/service.py](media_library/media_library/media/service.py) in the line 76 you can find a easy list comprehension.
Also, on the script [media_library/media_library/media/validator.py](media_library/media_library/media/validator.py) there is a validation using a List.

## Loop
On the script [media_library/media_library/main/router.py](media_library/media_library/main/router.py) in the line 35 there are a few For loops.

## Method
Well, there are a lot of them in the code. But in every instantiation of any class I implicitly used the constructor method __init__.
As you can see on the script [media_library/main.py](media_library/main.py) in the line 8.

## Class
Lot of classes everywhere.
The models are an example. Script [media_library/media_library/media/model.py](media_library/media_library/media/model.py) line 9.

## Interface
I think that I didn't use any interface. They are not common in Python 3. Probably I'm using it implicitly without knowing in any of the libraries that I imported.

## Encapsulation


## Abstraction


## Comment
There are some comments. I recommend you to look at the redocs when the software is running.  


## Inheritance
Every model inherit at least from a Base class from the DB.
Reference: [media_library/media_library/user/model.py](media_library/media_library/user/model.py) line 9.


## Polymorphism
Every time that we use the built-in method len() we are using polymorphism.

