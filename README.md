# Rudimentary API to demonstrate a deployable Flask application

This demo shows an example of a Flask application that implements a simple API. The application is containerized using Docker then deployed on the local machine and to Heroku.

In the creation of this project I learned a lot from the amazing [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xix-deployment-on-docker-containers) blog. This tutorial provides very clear explanations and insights into creating deployable Flask applications.

Although this demo was developed and tested on an Mac, the description is kept fairly generic for easy adaptability to other development platforms.

## Get the Application

Create a project directory, then clone the repository into it.

```bash
$ mkdir <project-directory> && cd <project-directory>
$ git clone https://github.com/atifar/miniapi.git .
```

The application requires Python 3.6 or later. The Python virtual environment is managed using `pipenv` in this project.

### Set Up the Virtual Environment Using Pipenv

Follow the pipenv [installation instructions](https://docs.pipenv.org/#install-pipenv-today) for your OS to install pipenv. Then install the app's dependencies by running the following command from the project directory.

```bash
$ pipenv install
```

To see the project's installed dependencies, run the following command:

```bash
$ pipenv graph
```

### Run All Tests (optional)

Execute the following command to run the tests for the application:

```bash
$ pipenv run pytest
```

The above command is used to run the tests inside the python virtual environment but without activating the virtual environment. Once the virtual environment has been activated (see next section), the command to run the tests becomes:

```bash
$ pytest
```

### Activate the Python Virtual Environment

The `pipenv shell` command activates the project's virtual environment in a new shell, and sets the environment variables listed in the `.env` file, therefore, the `FLASK_APP` environment variable will be set in this shell.

```bash
$ pipenv shell
```

### Run the Application Locally

Now run the application, served by the Flask development server, at the default port in your local machine, i.e. `localhost:5000`.

```bash
$ flask run
```
Access the API using an HTTP client such as `curl` or `Postman`. For instance,
```bash
$ curl -i -H "Accept: application/json" "localhost:5000/posts"
```
returns the array of all blog posts, which is just one entry.

```
HTTP/1.0 200 OK
...

[{"body":"hai","post_id":1,"title":"hai"}]
```

## API Usage

The application implements an API to create/delete/list blog post entries. The API consumes and produces data in JSON format.

### Creating a New Blog Post
  * URI path: `/post`
  * Request method: `POST`
  * Request body must include: `title` and `body` of the post (both ASCII strings)
  * Upon successful creation of the blog post the API returns a `201` status code and the created blog post entry.
  * Errors that prevent the creation of a blog post include:
    * Using a method other than `POST`. This results in an unsupported method response (status code `405`).
    * Omitting either `title` or `body` from the request or using a request content type other than `application/json`. The response contains an `error` key with a description of the error (status code `400`).

Example of a successful request:

```bash
curl -i -X POST -H "Content-Type: application/json" localhost:5000/post -d '{"title":"To be or not to be?", "body":"That is the question."}'
```

This returns:

```
HTTP/1.0 201 CREATED
...

{"title": "To be or not to be?", "body": "That is the question.", "post_id": 2}
```

Example of an incorrect request:

```bash
curl -i -X POST -H "Content-Type: application/json" localhost:5000/post -d '{"title":"To be or not to be?"}'
```

This returns:

```
HTTP/1.0 400 BAD REQUEST
...

{"error": "Please provide the body of the post!"}
```

### Listing All Blog Posts
  * URI path: `/posts`
  * Request method: `GET`
  * Using a method other than `GET`. This results in an unsupported method response (status code `405`).

Example:

```bash
$ curl -i -H "Accept: application/json" "localhost:5000/posts"
```

This returns:

```
HTTP/1.0 200 OK
...

[{"body":"hai","post_id":1,"title":"hai"},{"body":"That is the question.","post_id":2,"title":"To be or not to be?"}]
```

### Deleting a Blog Post
  * URI path: `/delete_post`
  * Request method: `DELETE`
  * Request must include the `id=<primary-key-of-post-to-delete>` query parameter.
  * Upon successful deletion of the blog post the API returns a `204` status code.
  * Errors that prevent the deletion of a blog post include:
    * Using a method other than `DELETE`. This results in an unsupported method response (status code `405`).
    * Omitting the blog post's `id` query parameter (status code `400`).
    * Using an `id` value for a non-existent blog post.

Example of a successful request:

```bash
$ curl -i -X DELETE -H "Accept: application/json" "localhost:5000/delete_post?id=2"
```

This returns:

```
HTTP/1.0 204 NO CONTENT
...
```

Example of trying to delete a non-existent blog post:

```bash
$ curl -i -X DELETE -H "Accept: application/json" "localhost:5000/delete_post?id=4"
```

This returns:

```
HTTP/1.0 404 NOT FOUND
...

{"error": "There is no blog post with id: 4 in the DB."}
```

## Deploying the Application Locally

The application is containerized using Docker in order to simplify the deployment process. We'll deploy the application to the local machine first, then to Heroku.

### Getting Docker

Docker CE has been used to develop this project. Make sure [Docker CE](https://www.docker.com/community-edition) is installed on your local machine and the docker daemon is running.

### Creating a Container Image

There is a Dockerfile in the project that contains the instructions for creating a Docker image. From the project's root directory (where the Dockerfile is) create a container image by running the following command (note the trailing `.`):

```bash
$ docker build -t miniapi:latest .
```

List the locally stored docker images, which now include `miniapi` and the base container image.

```bash
$ docker images
REPOSITORY                                   TAG                 IMAGE ID            CREATED             SIZE
miniapi                                      latest              2dcd35dd41ad        3 minutes ago       143MB
python                                       3.7-alpine3.7       ce56d42033a3        7 days ago          83.8MB
```

### Starting the Container Locally

The application inside the container is configured to listen on port 5000 by the `EXPOSE 5000` line in the Dockerfile and the gunicorn port binding in boot.sh (since the `PORT` environment variable is not set). When we start up the Docker container, we remap this port to 8000 as viewed from outside the container. This way the local API served by the Flask development server (at port 5000) and the containerized API running behind gunicorn inside a Docker container (accessed at port 8000) can coexist.

```bash
$ docker run --name miniapi -d -p 8000:5000 --rm miniapi:latest
40d1f61de02782ad80924cab19683799561e7ffa2066da8ea13f3b8ed0930937
```

The `docker run` command returned the container ID, which you can see in abbreviated form in the list of running containers.

```bash
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS                    NAMES
40d1f61de027        miniapi:latest      "./boot.sh"         About a minute ago   Up About a minute   0.0.0.0:8000->5000/tcp   miniapi
```

Now that the API is running in the container, we can test it by listing all blog posts:

```bash
$ curl -i -H "Accept: application/json" "localhost:8000/posts"
HTTP/1.1 200 OK
...

[{"body":"hai","post_id":1,"title":"hai"}]
```
It returned the only blog post that is seeded in the database.

## Deploying the Dockerized Application to Heroku

### Prerequisites

Make sure Docker is installed on your local machine! See the [Getting Docker](#getting-docker) section above for installation instructions.

Please sign up for a (free) Heroku account on the [Heroku](https://devcenter.heroku.com) website, unless you already have an account there.

We will be using the Heroku Command Line Interface in this deployment. Make sure it is installed on your local machine (see [Heroku CLI webpage](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) for instructions).

### Logging into Heroku

From the command line log into heroku with your email and password to obtain an API token:

```bash
$ heroku login
...
Logged in as <your email>
```

After a successful login an API token in stored in the `~/.netrc` file, which you can retrieve using the following command:

```bash
$ heroku auth:token
```

### Building and Pushing the Dockerized Application to Heroku

In order to deploy a dockerized application we need to log into Heroku's container registry:

```bash
$ heroku container:login
Login Succeeded
```

From the project's root directory (where the Dockerfile is) create a Heroku app. The app name, it's URL and git repo URL are generated by Heroku and shown in the output:

```bash
$ heroku create
Creating app... done, ⬢ <app_name>
https://<app_name>.herokuapp.com/ | https://git.heroku.com/<app_name>.git
```

The following command builds the Docker image of the application for Heroku, and pushes it to the container registry:

```bash
$ heroku container:push web
...
Your image has been successfully pushed. You can now release it with the 'container:release' command.
```

Release the image to the app:

```bash
$ heroku container:release web
... done
```

And the Flask application is now deployed to Heroku. We can test it with curl:

```bash
$ curl -i -H "Accept: application/json" "https://<app_name>.herokuapp.com/posts"
HTTP/1.1 200 OK
...

[{"body":"hai","post_id":1,"title":"hai"}]
```
