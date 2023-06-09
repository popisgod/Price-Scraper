from setuptools import setup


setup(
    name='scrape_prices',
    version='0.1.0',
    py_modules=['scrape_prices'],
    install_requires=[
        'click',
        'requests',
        'bs4',
        'tabulate',
        'fuzzywuzzy',
        'python-Levenshtein',
        'deep_translator'
    ],
    entry_points= {
        'console_scripts' : [
            'scrape_prices=scrape_prices:cli',
        ],
    },
)