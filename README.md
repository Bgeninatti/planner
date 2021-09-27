# Planner

A web app to select the best subset of tasks from a given list.

## How to run the app

1. Clone this repo

```
$ git clone https://github.com/Bgeninatti/planner
```

2. Enter in the `planner` directory

```
$ cd planner
```

### Using docker-compose.

3. Run docker-compose

```
$ docker-compose up
```

4. Go to `http://localhost:8000`

## Using a virtual environment


3. Create a virtualenv
```
$ python3 -m venv venv
```

4. Activate the virtualenv
```
$ source venv/bin/activate
```

5. Install the dependencies
```
$ pip install -r requirements.txt
```

6. Run the application using gunicorn
```
$ gunicorn --bind 0.0.0.0:8000 "planner.wsgi:application"
```

7. Go to `http://localhost:8000`

## How to use the app

1. Once the application is running go to `http://localhost:8000`

2. A form will be displayed with one input to upload a file.

3. The file must contain a JSON string in the following format:
```
[
    {
        "name": "some string",
        "resources": ["list", "of", "strings"],
        "payoff": 1.0
    }
    ...
]
```

Notice that each task is a dictionary with the following keys (no more, no less): `name`, `resources`, `payoff`

A few sample tasks files can be found [here](https://github.com/Bgeninatti/planner/tree/main/tests/sample_tasks).

4. Submit the form.

5. The result with the selected subset of tasks and excluded tasks will be displayed. 

## Running tests...

### using docker-compose

1. Run docker-compose inside the `planner` directory
```
$ docker-compose up -d
```

2. Open a bash shell inside the container
```
$ docker run -it planner_planner:latest bash
```

3. Run pytest inside the shell
```
/usr/src/app# pytest
```

### using virtual environment

1. Follow the steps in **Using a virtual environment** section up to step 5
2. Once inside the virtual environment run pytest
```
$ pytest
```
