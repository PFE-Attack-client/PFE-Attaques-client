# Server API for PFE - client attacks

## Purpose

This API is being developed for a student project in Cybersecurity at @Telecom SudParis.

## Installation

### Prerequisite:

- Having an instance of your database Running
- Having set up the .env variables

### Database init:
Then run the following commands only the first time ever you launch it:
```
    python3 manage.py initdb
    python3 manage.py migratedb
    python3 manage.py upgradedb
    python3 manage.py seeddb
```
    
## How to launch it?

```
    python3 manage.py test
    python3 manage.py run
```

## Authors
