# Rudimentary API to demonstrate a deployable Flask application

# Get the Application

Create a project directory, then clone the repository into it directory.

```bash
$ mkdir <project-directory> && cd <project-directory>
$ git clone https://github.com/atifar/miniapi.git .
```

The application requires Python 3.6 or later. The Python virtual environment may be created using `pipenv`. This is the method described in this documentation.

If you prefer to use Python's `venv` module to create the virtual environment, you can use the `requirements.txt` file in the repository to install the dependent Python packages. Use the approariate command to activate your virtual environment.

## Set Up Virtual Environment Using Pipenv

Follow the pipenv [installation instructions](https://docs.pipenv.org/#install-pipenv-today) for your OS to get pipenv. Then install the app's dependencies.

```bash
$ pipenv install
```

To see the project's installed dependencies, run the following command:

```bash
$ pipenv graph
```

## Run Application Locally

The following command activates the project's virtual environment in a new bash shell. It also sets the `FLASK_APP` environment variable in this shell.

```bash
$ pipenv shell
```
Now run the application, served by the Flask development server in your local machine.

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
Content-Type: application/json
Content-Length: 43
Server: Werkzeug/0.14.1 Python/3.7.0
Date: Mon, 30 Jul 2018 20:10:14 GMT

[{"body":"hai","post_id":1,"title":"hai"}]
```

# API Usage

The application implements an API to create/delete/list blog post entries. The API consumes and produces data in JSON format.

1. Creating a new blog post
  * URI path: `/post`
  * Request method: `POST`
  * Request body must include: `title` and `body` of the post (both ASCII strings)
  * Upon successful creation of the blog post the API returns a `204` status code and the created blog post entry.
  * Errors that prevent the creation of a blog post include:
    * Using a method other than `POST`. This results in an unsupported method response (status code `405`).
    * Omitting either `title` or `body` from the request. This returns the `error` key in the response with a description of the error (status code `400`).    


3. Listing all blog posts
  * URI path: `/posts`
  * Request method: `GET`
  * Using a method other than `GET`. This results in an unsupported method response (status code `405`).

2. Deleting blog post
  * URI path: `/delete_post`
  * Request method: `DELETE`
  * Request must include the `id=<primary-key-of-post-to-delete>` query parameter.
  * Errors that prevent the deletion of a blog post include:
    * Using a method other than `DELETE`. This results in an unsupported method response (status code `405`).
    * Omitting the blog post's id query parameter (status code `400`).
