from flask import Flask

app = Flask(__name__)

# safer way to fetch ENV
env = app.config.get("ENV", "development")

if env == "production":
    app.config.from_object("config.ProductionConfig")
elif env == "testing":
    app.config.from_object("config.TestingConfig")
else:  # default = development
    app.config.from_object("config.DevelopmentConfig")

from app import views
