

# STEPS TO RUN THE APPLICATION

# Clone the repository

    git clone https://github.com/e9kwagh/Everest.git

# Create a virtual environment

**For Linux and macOS**

    python3.8 -m venv venv
    source venv/bin/activate

**For Windows**

    pip install virtualenv
    python -m venv venv
    virtualenv venv
    venv/Scripts/activate

# Go inside the project folder

    cd 

# Install the necessary modules

    pip install -r requirements.txt

**If it shows error, run**

    pip install django

# Run the application

    python manage.py runserver

# Open the below url on your browser

     http://127.0.0.1:8000/


# You can also create a new super user with the following command and login with those credentials.
    python manage.py makemigration
    python manage.py migrate
    python manage.py createsuperuser
    