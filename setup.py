from setuptools import setup

setup(
    name='vinceladotcom',
    packages=['vinceladotcom'],
    include_package_data=True,
    install_requires=[
        'flask',
        'wtforms',     # Form validation
        'peewee',      # ORM
        'flask-login', # User management
        'passlib',     # Hashing
        'mistune',     # Markdown Parsing
        'pytest'
    ],
)