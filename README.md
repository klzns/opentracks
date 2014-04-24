opentracks
==========

## Setup

First, build Open-Transactions system wide with the Python flag on.

Setup a virtual environment

```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate
``` 

Install dependencies

```bash
pip install -r Requirements.txt
```

## Running

Do this once

```bash
source venv/bin/activate
```

Then

```bash
python app/webapp.py
```

Open your browser at [http://localhost:5000/](http://localhost:5000/)

When you're done working, remember to deactivate the virtual environment

```bash
deactivate
```

## Desktop

Install PySide if you want to run the desktop version (QT).

Follow this instructions: [https://pypi.python.org/pypi/PySide](https://pypi.python.org/pypi/PySide)

Then

```bash
python app/opentracks.py
```

