## CSE 5330 Project 2 Part 2

Project is a Python Flask app for CSE 5330 Database Course at UTA

To run the project

- Install [Python](https://www.python.org/downloads/)

- To install project dependencies, open a Terminal/CMD in project dir and execute
```bash
pip install -r requirements.txt
```

- Use the `cse5330_db_dump.sql` to set up your DB.

- Enter your DB connection string in the `.env` file for the `SQLALCHEMY_DATABASE_URI` variable.

- To run the project, execute from project directory
```bash
flask run
```

- Navigate to [http://localhost:5000](http://localhost:5000) and see the application


The application is deployed on heroku.
__You can view the deployed app by clicking [here](https://turaga-cse5330-project2.herokuapp.com/db_app/).__
