# incubyte-assignment
Incubyte - Data Engineer assignment

## Usage
- Run `pip install -r requirements.txt` to install dependencies.
- `cd` into `src` directory and run `python main.py` for the script that populates the tables into the database (based on country segregation).
- `cd` into `src` directory and run `python tests.py` to run the unit-tests for the segregation logic.

## Notes
- I would prefer to use a context manager to close the database connection in a production-level codebase.
- If you try to populate the database multiple times, it will fail. I have set it to fail for now. I can make sure it appends records in the demo.
- I would like to conduct a demo of the code for better clarity.
