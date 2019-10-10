"""
Main module of the server file
"""

from flask import render_template
import config


# Get the application instance
connex_app = config.connex_app
print("at server - before swagger.yml")
# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")

print("at server - after swagger.yml")
# create a URL route in our application for "/"
@connex_app.route("/")
def home():
    return render_template("home.html")

print("at server - after return")

if __name__ == "__main__":
    connex_app.run(debug=True)