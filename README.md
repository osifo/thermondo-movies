# Backend Senior Coding Challenge 🍿

In this challenge, I designed and implemented a robust
backend system that handles user interactions and provides movie ratings. We
don't want to check coding conventions only.

## ✅ Requirements

- [x] The backend should expose RESTful endpoints to handle user input and
      return movie ratings.
- [x] The system should store data in a database. You can use any existing
      dataset or API to populate the initial database.
- [x] Implement user endpoints to create and view user information.
- [x] Implement movie endpoints to create and view movie information.
- [x] Implement a rating system to rate the entertainment value of a movie.
- [x] Implement a basic profile where users can view their rated movies.
- [x] Include unit tests to ensure the reliability of your code.
- [x] Ensure proper error handling and validation of user inputs.

## ✨ Bonus Points

- [x] Implement authentication and authorization mechanisms for users.
- [x] Provide documentation for your API endpoints using tools like Swagger.
- [x] Implement logging to record errors and debug information.
- [ ] Implement caching mechanisms to improve the rating system's performance.
- [ ] Implement CI/CD quality gates.

# Solution Notes

### How to launch the app

1. Clone the repository
2. copy the `.env.example` and `alembic.ini.example` files to new `.env` and `alembic.ini` files respectively.
3. Update the files from step 2 above.

- in `.env`, populate values for `DB_USERNAME` and `DB_PASSWORD`
- in `alembic.ini` update the `sqlalchemy.url` key, populating the values for `username` and `password`

4. Install docker-desktop (if you do not have docker installed)
5. Setup the application: run `docker compose up --build`. (You might need to use sudo for this)
6. You should be able to access the app on the port displayed in your terminal (should be localhost:4000).

### How to test the functionality

First you'd need to run migrations

1. run `docker ps` to get the id of the container running the api
2. access the terminal of this container to run database migration
   a. to access the terminal, run `docker exec -it <container_id> bash`
   b. once inside the container you should be in the /app dir), run migrations using: `alembic upgrade head`
3. You test the app's functionality via the swagger documentation available on the `/docs` route (e.g `http://localhost:4000/docs`).

### Running tests:

To run tests, run: `python -m APP_ENV=test pytest tests/`

### Areas for Improvement

[ ] Finish setup of CI/CD using github workflows
[ ] Use [wait-for-it.sh](https://github.com/vishnubob/wait-for-it) to eliminate the need to run migrations manually during docker setup.
[ ] Complete redis setup and integrate with the movie rating logic
[ ] Write tests for the repositories and models
[ ] Use orjson to improve json serialization speed

### Other notes

- Technical debts in code are denoted with `TO-DO` comments.
- Notes for reviewers are denoted with `DEV-NOTE` comments.
