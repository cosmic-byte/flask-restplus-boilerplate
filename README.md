Flask RESTful API boiler-plate with JWT
=======================================

Fork
----

The current example source code is available at:  
https://github.com/olibre/flask-restplus-boilerplate

This is a fork from the original Git repository:  
https://github.com/cosmic-byte/flask-restplus-boilerplate


Motivation
----------

In my current example, source code (files) is organized by ressources (end points) instead of by Model/Controller/Service.
The motivation is to facilitate the exploration of the source code by keeping a link between API documentation and file organization.

Each sub directory corresponds to a namespace.
Within each namespace the source code is organized between:
    
* Model (database)
* Controller (ressources/end-points)
* Service (business logic)
* DTO (Data Transfert Object)


Install Pipenv
--------------

The project uses `pipenv` to manage dependencies and virtual environment.

    python3 -m pip install pipenv --user --upgrade


Install dependencies
--------------------

Main dependencies are stored in the [`Pipfile`](./Pipfile).

```c
$ python3 -m pipenv install
Creating a virtualenv for this project…
Pipfile: /home/b/Documents/oli/job/sesam/flask-restplus-boilerplate/Pipfile
Using /usr/bin/python3 (3.7.3) to create virtualenv…
⠦ Creating virtual environment...Already using interpreter /usr/bin/python3
Using base prefix '/usr'
New python executable in /home/b/.local/share/virtualenvs/flask-restplus-boilerplate-__tG4DC_/bin/python3
Also creating executable in /home/b/.local/share/virtualenvs/flask-restplus-boilerplate-__tG4DC_/bin/python
Installing setuptools, pip, wheel...
done.

✔ Successfully created virtual environment! 
Virtualenv location: /home/b/.local/share/virtualenvs/flask-restplus-boilerplate-__tG4DC_
Pipfile.lock not found, creating…
Locking [dev-packages] dependencies…
✔ Success! 
Locking [packages] dependencies…
✔ Success! 
Updated Pipfile.lock (712423)!
Installing dependencies from Pipfile.lock (712423)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 26/26 — 00:00:03
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```

For the unit-tests, install one more dependency using the `--dev` option:

```c
python3 -m pipenv install --dev
Installing dependencies from Pipfile.lock (712423)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 27/27 — 00:00:02
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```


Print help
----------

```c
$ python3 -m pipenv run python3 -m api
usage: __main__.py [-?] {db,test,shell,runserver} ...

positional arguments:
  {db,test,shell,runserver}
    db                  Perform database migrations
    test                Runs the unit tests.
    shell               Runs a Python shell inside Flask application context.
    runserver           Runs the Flask development server i.e. app.run()

optional arguments:
  -?, --help            show this help message and exit
```


Check unit-tests
----------------

```c
$ python3 -m pipenv run python3 -m api test
test_non_registered_user_login (api.test.test_auth.TestAuthBlueprint)
Test for login of non-registered user ... email or password does not match.
ok
test_registered_user_login (api.test.test_auth.TestAuthBlueprint)
Test for login of registered-user login ... ok
test_registered_with_already_registered_user (api.test.test_auth.TestAuthBlueprint)
Test registration with already registered email ... ok
test_registration (api.test.test_auth.TestAuthBlueprint)
Test for user registration ... ok
test_valid_blacklisted_token_logout (api.test.test_auth.TestAuthBlueprint)
Test for logout after a valid token gets blacklisted ... ok
test_valid_logout (api.test.test_auth.TestAuthBlueprint)
Test for logout before token expires ... ok
test_app_is_development (api.test.test_config.TestDevelopmentConfig) ... ok
test_app_is_production (api.test.test_config.TestProductionConfig) ... ok
test_app_is_testing (api.test.test_config.TestTestingConfig) ... ok
test_decode_auth_token (api.test.test_user_model.TestUserModel) ... ok
test_encode_auth_token (api.test.test_user_model.TestUserModel) ... ok

----------------------------------------------------------------------
Ran 11 tests in 2.957s

OK
```

Start web server
----------------

```c
$ python3 -m pipenv run python3 -m api runserver
 * Serving Flask app "api.main.api" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 243-684-679
127.0.0.1 - - [17/Sep/2019 20:48:39] "GET /robots.txt HTTP/1.1" 404 -
127.0.0.1 - - [17/Sep/2019 20:48:40] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [17/Sep/2019 20:48:40] "GET /swaggerui/droid-sans.css HTTP/1.1" 200 -
127.0.0.1 - - [17/Sep/2019 20:48:40] "GET /swaggerui/swagger-ui.css HTTP/1.1" 200 -
127.0.0.1 - - [17/Sep/2019 20:48:40] "GET /swaggerui/swagger-ui-bundle.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Sep/2019 20:48:40] "GET /swaggerui/swagger-ui-standalone-preset.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Sep/2019 20:48:40] "GET /swaggerui/swagger-ui.css HTTP/1.1" 200 -
127.0.0.1 - - [17/Sep/2019 20:48:41] "GET /swaggerui/favicon-16x16.png HTTP/1.1" 200 -
127.0.0.1 - - [17/Sep/2019 20:48:41] "GET /swagger.json HTTP/1.1" 200 -
```

Open http://127.0.0.1:5000/ on your browser to view OpenAPI (Swagger) documentation.


Migrate SQL database shema
--------------------------

To migrate from one database shema to another one, please follow instructions from command line:

```c
python3 -m pipenv run python3 -m api db
usage: Perform database migrations

Perform database migrations

positional arguments:
  {init,revision,migrate,edit,merge,upgrade,downgrade,show,history,heads,branches,current,stamp}
    init                Creates a new migration repository
    revision            Create a new revision file.
    migrate             Alias for 'revision --autogenerate'
    edit                Edit current revision.
    merge               Merge two revisions together. Creates a new migration
                        file
    upgrade             Upgrade to a later version
    downgrade           Revert to a previous version
    show                Show the revision denoted by the given symbol.
    history             List changeset scripts in chronological order.
    heads               Show current available heads in the script directory
    branches            Show current branch points
    current             Display the current revision for each database.
    stamp               'stamp' the revision table with the given revision;
                        don't run any migrations

optional arguments:
  -?, --help            show this help message and exit


$ python3 -m pipenv run python3 -m api db init
  Creating directory /home/olibre/flask-restplus-boilerplate/migrations ... done
  Creating directory /home/olibre/flask-restplus-boilerplate/migrations/versions ... done
  Generating /home/olibre/flask-restplus-boilerplate/migrations/script.py.mako ... done
  Generating /home/olibre/flask-restplus-boilerplate/migrations/env.py ... done
  Generating /home/olibre/flask-restplus-boilerplate/migrations/alembic.ini ... done
  Generating /home/olibre/flask-restplus-boilerplate/migrations/README ... done
  Please edit configuration/connection/logging settings in '/home/olibre/flask-restplus-boilerplate/migrations/alembic.ini' before proceeding.
```


### Details about Pipenv

Pipenv is a simple tool based on Pip and VirtualEnv.
To generate the [`Pipfile`](./Pipfile) use the two following commands:

```c
$ python3 -m pipenv install flask_migrate flask_restplus flask_script flask_bcrypt PyJWT
Installing flask_migrate…
Adding flask_migrate to Pipfile's [packages]…
✔ Installation Succeeded 
Installing flask_restplus…
Adding flask_restplus to Pipfile's [packages]…
✔ Installation Succeeded 
Installing flask_script…
Adding flask_script to Pipfile's [packages]…
✔ Installation Succeeded 
Installing flask_bcrypt…
Adding flask_bcrypt to Pipfile's [packages]…
✔ Installation Succeeded 
Installing PyJWT…
Adding PyJWT to Pipfile's [packages]…
✔ Installation Succeeded 
Pipfile.lock (dd33d3) out of date, updating to (7d7e84)…
Locking [dev-packages] dependencies…
Locking [packages] dependencies…
✔ Success! 
Updated Pipfile.lock (dd33d3)!
Installing dependencies from Pipfile.lock (dd33d3)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 26/26 — 00:00:02
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```

```c
$ python3 -m pipenv install --dev flask_testing
Installing flask_testing…
Adding flask_testing to Pipfile's [dev-packages]…
✔ Installation Succeeded 
Pipfile.lock (960202) out of date, updating to (dd33d3)…
Locking [dev-packages] dependencies…
✔ Success! 
Locking [packages] dependencies…
✔ Success! 
Updated Pipfile.lock (960202)!
Installing dependencies from Pipfile.lock (960202)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 27/27 — 00:00:02
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```


Using Postman
-------------

Authorization header is in the following format:

    Key: Authorization
    Value: "token_generated_during_login"

For testing authorization, URL for getting all user requires an admin token while URL for getting a single
user by `{public_id}` requires just a regular authentication.


Full description and guide
--------------------------

https://medium.freecodecamp.org/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563


Contributing
------------

If you want to contribute to this flask restplus boilerplate:

1. Create a personal [fork](https://help.github.com/articles/fork-a-repo/#fork-an-example-repository) of [this repo](./).
2. [Clone](https://help.github.com/articles/fork-a-repo/#step-2-create-a-local-clone-of-your-fork) your forked Git repo using for example  
   `git clone git@github.com:{USERNAME}/flask-restplus-boilerplate`
3. Create a new branch `git checkout -b my-new-branch` (optional)
4. Perform your change
5. Commit you change using for example  
   `git commit -m '{Verb something...}' file1 file2...` 
6. Push you commit to remote Git repository using for example  
   `git push --set-upstream origin {branch-name}` or simply `git push`
7. Go back to GitHub and initiate a Pull Request  
   [{USERNAME}/flask-restplus-boilerplate/pull/new/](https://github.com/{USERNAME}/flask-restplus-boilerplate/pull/new/)

See also step-by-step explanation at https://github.com/LearnFrontEnd/fork-me
