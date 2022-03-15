# spider-network
Example of using cytoscape to draw an electrical network.  See it in [action](https://spider-network.herokuapp.com/)

## Data

See example data:

  - `data\edges.csv`
  - `data\nodes.csv`

  To load into database:


    
## Heroku

To start the app locally in dev mode:

  export FLASK_APP=app
  FLASK_ENV=development
  flask run

In prod mode:

  gunicorn wsgi:app

To deploy it, push it to github.