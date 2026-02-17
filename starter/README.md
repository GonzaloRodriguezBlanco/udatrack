# Udatracker

TDD demo project in python. There is an order tracker service which is an application service to include the CRUD logic 
operations. These operations raise errors for edge cases which are captured in the user|api layer to map to http error 
responses in addition to the success responses. Some of the features, like the implementation of '*List order status*' 
was also an opportunity to refactor the code about status validation in order to avoid duplicated code.

Although it was not required, one additional test was included in the integration tests for the '*Add order error response*'.
As next steps it could be good to cover the api layer integration tests with all the http error cases.

```
.
├── backend
│   ├── __init__.py
│   ├── app.py
│   ├── in_memory_storage.py
│   ├── order_tracker.py
│   ├── requirements.txt
│   └── tests
│       ├── __init__.py
│       ├── test_api.py
│       └── test_order_tracker.py
├── frontend
│   ├── css
│   │   └── style.css
│   ├── index.html
│   └── js
│       └── script.js
├── pytest.ini
└── README.md
```

## Local development setup

```shell
# Clone the starter repository
git clone https://github.com/GonzaloRodriguezBlanco/udatrack.git
cd udatrack/starter

# Create and activate virtual environment
python3 -m venv venv 
source venv/bin/activate

# Install dependencies from requirements.txt
pip install -r backend/requirements.txt

# Run the Flask app
python -m backend.app

# Open your web browser and go to http://127.0.0.1:5000  
```

## Running Tests

```shell
# Run all tests
pytest

# Run only unit tests
pytest backend/tests/test_order_tracker.py

# Run only integration tests
pytest backend/tests/test_api.py

# Run a single test function by name
pytest -k test_add_order_api_success
