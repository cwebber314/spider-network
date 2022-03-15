# spider-network

Example of using cytoscape to draw an electrical network.  See it in action [here](https://spider-network.herokuapp.com/)

This app is setup to use both sqlite and postgres.

To start the sqlite version of the app:
```
python app_sqlite.py
```

To start using the postgres database use:
```
python app_postgres.py
```

## Local Postgres setup

For the local postgres:
```
export DATABASE_URL=postgres://flask:nomoresecrets@localhost:5432/spider
```

Create the user:

```
sudo -u postgres -i
psql
CREATE USER username;
ALTER USER username WITH SUPERUSER;
```

Now as the normal user:
```
createdb spider
psql -d spider
```

Setup a low privilidge user for the web application:
```
CREATE USER flask;
ALTER USER flask PASSWORD 'nomoresecrets';
GRANT SELECT, UPDATE, INSERT, DELETE ON ALL TABLES IN SCHEMA public TO flask;
```

Granting permissions on PROCs can only be done one at a time:
```
GRANT EXECUTE ON PROCEEDURE procname TO role;
``` 

pgAdmin crashes when I start the query tool - dbeaver should be a good
tool for running queries. 

## Heroku Postgres setup

Use the `DATABASE_URL` in the heroku config vars.  Fetch the data like this:

```
exprot DATABASE_URL=$(heroku config:get DATABASE_URL -a spider-network)
```

To push the local database use:
```
heroku pg:reset --confirm spider-network
heroku pg:push spider DATABASE_URL --app spider-network
```

To open a psql quick connection to the heroku database:
```
TODO
```

## Data Load local (postgres)

To load the data on the local instance use the `copy_test.sql`.

## Heroku

To start the app locally in dev mode:

  export FLASK_APP=app
  FLASK_ENV=development
  flask run

In prod mode:

  gunicorn wsgi:app

To deploy it, push it to github.

