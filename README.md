# cars-api

Simple REST API developed using Django Rest Framework for recruitment purposes. It makes use of an external API to verify whether the given car exists or not.

## Preview

The application was deployed to Heroku and it is accessible [here](https://glacial-taiga-71851.herokuapp.com/).

## Running locally 
1. Clone the repository
`git clone https://github.com/fiedosiukr/cars-api`
2. Build the images
`docker-compose build`
3. Start the project
`docker-compose up`
4. The project is accessible under `localhost:8000`

## Notes
- when a car is already in the database, it is not duplicated
- to run the tests, use `make test`
- `black` and `isort` were used for formatting
- `whitenoise` is used for file serving
- `gunicorn` is used in the production environment
- the repository doesn't contain all of the production setup
- `pydantic` is used for the response validation