"""to start an app"""
import sys
from abdieapp import app

if __name__ == "__main__":
    app.run(debug=True, port=8080)
    