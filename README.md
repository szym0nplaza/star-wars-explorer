# Star Wars explorer

- [Introdution](#introdution)
- [Plans to optimize app](#for-future)
- [Setup](#setup)


<a name="introdution"></a>
## Introdution
App for collecting datasets from SWAPI, includes tables review and filtering

I decided to use simplified domain centric design for better module separation

**Note!**

**Collecting data speed can differ based on your computer and network bandwidth**

<a name="for-future"></a>
## Optimization plan
    - Write tests for services
    - Put requests to some task queue (e.g. Celery)
    - Prepare app for API changes (new data etc.)
    - Consider what is better for storing repetable data
    - Add docker for faster development

<a name="for-future"></a>
## Setup
Required Python version: **3.9**

**Note!**

If there will be any problems try to set ```export PYTHONPATH=./src``` for your local env in your terminal
(can occur during migrations)

1. Create virtual enviroment (```python -m venv env```)
2. Install requirements (```env/bin/pip install -r requirements/base.txt```)
3. Run migrations to db (```env/bin/python manage.py migrate```)
4. Run app (```env/bin/python manage.py runserver```)

## Screenshots
![Alt text](https://github.com/szym0nplaza/star-wars-explorer/blob/main/screenshots/s2.png)
