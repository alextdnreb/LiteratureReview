## Introduction
This repository contains utilities to query the [dblp API](https://dblp.org/faq/How+to+use+the+dblp+search+API.html) for scientific publications and filter the publications based on [CORE conference rankings](https://portal.core.edu.au/conf-ranks/?search=COMPLEX+NETWORKS+2018&by=all&source=CORE2023&sort=atitle&page=1).

The file `search_utils.py` contains the actual utility functions for querying and filtering; `survey_manufacturing.ipynb` and `slr_disentangled.ipynb` contain two examples on how to use the functionality. 

## Install
1. create a virtual environment
```bash
python -m venv venv
```
2. install the requirements as defined in the requirements.txt
```bash
    pip install -r requirements.txt
```
