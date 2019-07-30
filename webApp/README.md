# Use Flask to interact with your IoT functions
In this webApp demo, we implemented (visualized) the fund transfer example among all the functions we created. The demo currently only runs on the same server, raspi is not supported yet. A  re-deisnged full functional Web App/IOS app will be released late this year to onboard non-tech users to experience EVEC IoT solution.

## Prerequisites
In order to run flask, make sure you `pip install flask`, `pip install Flask-API`.

## run the code

* In your terminal, `cd` to this `webApp` folder.
* Run `python flask-api.py`, If see error relates to missing module, `pip install [module-name]`
* Open Browser in `http://0.0.0.0:5000`, then enter your account info to transfer fund (make sure your account balance is sufficient). 
* In order to run the react front end, please follow the instruction in `front-end/evec`. You need to have `npm` installed the npm packages. 