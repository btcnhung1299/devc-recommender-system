# ChoTot Recommender System

This repository is a team project to build a recommender system for Devoloper Circles Innovation Challenge: Ho Chi Minh City.

# Get Started

## Prerequisite:
- Python >= 3.6
- Pip

## Setup virtual environment:
1. Install virtualenv 
```console
pip install virtualenv
```

2. Clone the repository
```console
git clone https://github.com/btcnhung1299/devc-recommender-system.git
```

3. Create and activate virtual environment inside the clone repo
```console
virtualenv venv -p python3
source venv/bin/activate
```

4. Install necessary libraries & packages
```console
pip install -r requirements.txt
```

5. Start flask server under chotot_recommendersys folder

```console
cd chotot_recommendersys
flask run
```

# Data Schema
<img src="./database/db_schema.png" height="270">

# API Reference
See more at [API Document](./api_reference.md).
