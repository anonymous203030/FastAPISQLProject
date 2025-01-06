# FASTAPI SQL BASIC APPLICATION

## Step 0: Git clone repository to your local env and get into dir

```
git clone https://github.com/anonymous203030/FastAPISQLProject.git
cd FastAPISQLProject
```

## Step 1: Create Python environment and install dependencies

> [!WARNING]
> _if no Python, install from [Download Python](https://www.python.org/downloads/) concerning to your specific OS_

### **Linux**

```
python3 create_venv.py
```

### **Windows**

```
python create_venv.py
```

## Step 2: Test run

```
uvicorn main.main:app --reload
```

### This command will run local uvicorn web server in your computer

> [!NOTE]
> Ctrl+C to quit

## Step 3: Create SQLite local database

### Run script to make init_db.sql file initialize DB.

```
python3 -m main.main
```

< [!NOTE]
> This command will create sqlite3 database file called books.db and the models created in models.py
