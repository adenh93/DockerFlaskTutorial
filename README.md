## Purpose

I will be using this repository to learn the odds and ends of the Python Flask Framework.
I will be building a mock application with an SQLlite database connection fit with Migrations.

In this project, I also hope to showcase my understanding of the Flask framework, by means of implementing *clean templating* with Jinja, a *secure API*, *basic user authentication*, *_oAuth_*, *Role-based access control (RBAC)* and more. 

## Environment
I am building this project in a Linux-based environment (Ubuntu 18.04.2 LTS), with Docker, Python3 and the latest Flask framework.

## How to build
Before you can build this project, you will need to ensure that your Python3 version is up to date (3.6.7 at the current time), install Pip3 and virtualenv.
You will also need to install Docker on your machine.

With these requirements met, you can do the following:

1. Clone the repo
2. Open a terminal instance in the cloned repository
3. Create your virtualenv via `virtualenv env`
4. Activate the env via `source env/bin/activate`
5. Install all dependencies via `pip3 install -r requirements.txt`
6. Install the database and the latest migrations via `sh migrate-up.sh`.
7. Run the application via `sh run.sh`

## Future plans
In the future, I aim to implement a modern Javascript framework on the client, such as Aurelia, Angular or React/Inferno.
