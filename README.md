#### FLASK RESTFUL API BOILER-PLATE WITH JWT

Initial run: pip install -r requirements.txt

To run test: python manage.py test

To run application: python manage.py run


### Running the app ###

Open the following url on your browser to view swagger documentation
http://127.0.0.1:5000/


### Using Postman ####

Authorization header is in the following format:

Key: Authorization
Value: "token_generated_during_login"

For testing authorization, url for getting all user requires an admin token while url for getting a single
user by public_id requires just a regular authentication.
