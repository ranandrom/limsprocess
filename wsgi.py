import sys

# Expand Python classes path with your app's path
sys.path.insert(0, "c:/Test_Web")

from runserver import app

# Put logging code (and imports) here ...

# Initialize WSGI app object
application = app

