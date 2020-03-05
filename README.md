# Boggle

[![Build Status](https://travis-ci.com/gianghta/Boggle.svg?branch=master)](https://travis-ci.com/gianghta/Boggle)
[![Python versions](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue)](
https://www.python.org)

Boggle is a word game that is played on a 4x4 board with 16 letter tiles.
The goal is to find as many words as possible given a time constraint.
For this exercise, we are making one modification.
Now it is possible for one or more of the letter tiles to be blank (denoted by `*`).
When a tile is blank, it can be treated as any other letter.
Note that in one game it does not have to be the same character for each word.
For example, if the tiles C, T, and * are adjacent. The words cot, cat,
and cut can all be used.  You will be given a text file containing all
valid English words (a dictionary). You will also be given an initial board
configuration as a text file with commas separating the letters.
Use this as a guide for how to set up the board.

For example, a file may contain:

```
A, C, E, D, L, U, G, *, E, *, H, T, G, A, F, K
```

This is equivalent to the board:

```
A C E D
L U G *
E * H T
G A F K
```

Some sample words from this board are ace, dug, eight, hole, huge, hug, tide.

## Getting started

1. Ensure [Docker](https://www.docker.com) is installed and running

2. Install [Poetry](https://github.com/python-poetry/poetry)
```
pip install poetry
```

3. Run the project
```
./scripts/dev.sh
```
The application will be running at http://locahost:8000

## Documentation

After running the application, the API documentation will be available at http://localhost:8000/docs

## Testing

#### 1. Run the tests

```
./scripts/test.sh
```

#### 2. Run the tests provided by [Saleswhale](https://www.saleswhale.com/)

- Install [Ruby](https://www.ruby-lang.org/en/downloads)

- Install [Ruby Bundler](https://bundler.io)

- Install [gem](https://rubygems.org/pages/download)

- Edit `saleswhale\.env` file and replace sample `SERVER_URL` with your server url

- Then run the commands:
  ```
  cd saleswhale

  # Install the dependencies for testing
  bundle install

  # Run test:
  rspec
  ```

## Explanation

#### 1. [Docker](https://www.docker.com/)
  - Used for environment isolation and deployment container

#### 2. [Tox + Travis CI](https://travis-ci.org/)
  - Used for setting up dev environment, test environment
  - Check code style and pre-commit
  - Integrating CI/CD

#### 3. [Poetry](https://python-poetry.org/)
  - Package manager of the project

#### 4. [Alembic](https://alembic.sqlalchemy.org/en/latest/)
  - Database migration tool

#### 5. Schema ([Marshmallow](https://marshmallow.readthedocs.io/en/stable/))
  * Used for data validation and data serialization from input and output source
  * Created 3 schemas Get/Write/Out:
    1. Get: Validate input to query from database model
    2. Write: Serialize and validate data from client request that meant to change or add data into database, preventing unwanted modification
    3. Out: Serialize and filter data before returning to client

#### 6. function ```validate_request```
  - A decorator used to load `body`, `path`, `params` and query params from request to validate required attributes, using `READ` schema

    ```
    @validate_request(model="Board", method="Read")
      async def get(self, *args, path_params=None, body=None, query_params=None, **kwargs):
    ```
#### 7. function ```serialize_output```
  - A decorator used to serialize output before returning response to client

    ```
    @serialize_response(model="Board", status_code=201)
      async def create_game(request):
    ```

#### 8. function ```authenticate```
  - A decorator used to check of matching token and ID number for correct return data, using `path_params` and `body` returned by `validate_request`

    ```
    @validate_request(model="Board", method="Read")
    @authenticate
      async def put(self, *args, path_params, body, **kwargs):
    ```