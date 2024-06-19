
This project demonstrates a deisgn and implementartion of a robust
backend system that handles user interactions and provides movie ratings. 

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
- [x] Implement authentication and authorization mechanisms for users.
- [x] Provide documentation for your API endpoints using tools like Swagger.
- [x] Implement logging to record errors and debug information.


### How to setup the app locally

1. Clone the repository
2. In the app's root directory, copy the `.env.example` and `alembic.ini.example` files to new `.env` and `alembic.ini` files respectively.
3. Update the files from step 2 above.

- in `.env`, populate values for `DB_USERNAME` and `DB_PASSWORD`
- in `alembic.ini` update the `sqlalchemy.url` key, populating the values for `username` and `password`

4. Install docker-desktop (if you do not have docker installed)
5. While in the app root directory, setup the application by runnning: `docker compose up --build`. (You might need to use sudo for this)
6. You should be able to access the app on the port displayed in your terminal (this should be localhost:4000).

### How to run the app

First you'd need to run migrations
1. Run `docker ps` to get the id of the container running the api
2. Run database migration by takingn the following steps:
   - a. run `docker exec -it <container_id> bash` to access the container terminal.
   - b. once inside the container (you should be in the /app dir), run migrations using: `alembic upgrade head`
3. You can test the app's functionality via the swagger documentation available on the `/docs` route (e.g `http://localhost:4000/docs`).

### How to test the features

**NOTE**
- _Two user roles exist: `admin` and `basic`; Admin users can create other users._
- _The `/create_user` endpoint requires the user to be authenticated and authorized._

1. Sign up using the `/signup` endpoint
2. With your email, id and token in the response, you can then perform other actions.

### Running tests:

To run tests
- install test requirements, run: `pip install -r requirements_test.txt`
- run test cases, run: `python3 -m APP_ENV=test pytest tests/`

### Areas for Improvement
- [ ] Complete integration test converage for every routem cover the edge cases
- [ ] Write tests for the repositories and models
- [ ] Setup CI/CD using github workflows
- [ ] Add pyright in CI step to check that best typing practices are adhered to.
- [ ] Use [wait-for-it.sh](https://github.com/vishnubob/wait-for-it) to eliminate the need to run migrations manually during docker setup.
- [ ] Complete redis setup and integrate with the movie rating logic
- [ ] Use orjson to improve json serialization speed

### Other notes

- Technical debts in code are denoted with `TO-DO` comments.
- Notes for reviewers are denoted with `DEV-NOTE` comments.
