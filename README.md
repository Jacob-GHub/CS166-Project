# CS166-Project

## How to set it up

```bash
cs166_initdb
cs166_db_start
cs166_createdb $USER'_project_DB'
cs166_psql $USER'_project_DB' < create_tables.sql
cs166_psql $USER'_project_DB' < indexes.sql
cs166_psql $USER'_project_DB' < seed_data.sql
```

## Running it

```bash
python main.py $USER'_project_DB' $PGPORT $USER
```

## Files

- `create_tables.sql` — schema (provided)
- `indexes.sql` — indexes for performance tuning
- `seed_data.sql` — sample data that chatgpt made
- `main.py` — CLI interface
- `queries.py` — all SQL operations

## Test Accounts after running the seed data

| Login | Password | Role |
|-------|----------|------|
| admin1 | admin123 | Admin |
| alice | pass1234 | Seller |
| dave | pass1234 | Buyer |
