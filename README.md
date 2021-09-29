# See My Vest!

https://www.youtube.com/watch?v=TyWVaZsUQjc

A program to calculate vesting schedules.

I chose not to use coroutines as most operations are CPU-bound as opposed to IO-bound, and the main IO operation has a 
global ordering requirement.

## Environment setup:

Dependencies managed via Poetry: https://python-poetry.org/

Once installed:
```
poetry install
poetry shell
```

## How to run:
```
python see_my_vest.py  --help
python see_my_vest.py tests/csv_data/example3.csv 2020-04-01 0

```