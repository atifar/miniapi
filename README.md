# Rudimentary API to demonstrate a deployable Flask application

## Get the Application

Create a project directory, then clone the repository into it directory.

```bash
$ mkdir <project-directory> && cd <project-directory>
$ git clone https://github.com/atifar/miniapi.git .
```

The application requires Python 3.6 or later. The Python virtual environment may be created using `pipenv`. This is the method described in this documentation.

If you prefer to use Python's `venv` module to create the virtual environment, you can use the `requirements.txt` file in the repository to install the dependent Python packages. Use the approariate command to activate your virtual environment.

### Set Up the Virtual Environment Using Pipenv

Follow the pipenv [installation instructions](https://docs.pipenv.org/#install-pipenv-today) for your OS to get pipenv. Then install the app's dependencies.

```bash
$ pipenv install
```

To see the project's installed dependencies, run the following command:

```bash
$ pipenv graph
```

### Run Application Locally

The following command activates the project's virtual environment in a new bash shell. It also sets the `FLASK_APP` environment variable (see the `.env` file) in this shell.

```bash
$ pipenv shell
```
Now run the application, served by the Flask development server at the default port in your local machine, i.e. `localhost:5000`.

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
