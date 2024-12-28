# TheBoxVault

# Run this command to run ngrok to expose the local Flask app to the internet and to be able to access it from your phone at home:

ngrok http 5003

# Activate venv environment:

  python3 -m venv venv

  source venv/bin/activate

# If it's the first time running the app run this command to install the necessary libraries: 

  pip install flask flask-sqlalchemy qrcode pillow

# Run the actual Flask app: 

  python3 app.py
