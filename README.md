![](http://i.imgur.com/p8bnuiZ.png) Open Tracks
==========

## Setup

First, build Open-Transactions system wide with the Python flag on. You can check its [docs here](https://github.com/Open-Transactions/Open-Transactions/tree/master/docs) for more info.

Setup a virtual environment

```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate
``` 

Install dependencies

```bash
pip install -r requirements.txt
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

## REST API

[REST API Docs](http://api-portal.anypoint.mulesoft.com/raml/console?raml=http://api-portal.anypoint.mulesoft.com/open-tracks/api/open-tracks-rest-api/OpenTracks.raml) (under development)


-----

<sub>Logo: Interchange by Laurent Patain from The Noun Project</sub>
