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

### This command will run your fastapi server on port 8080

```
fastapi dev main/main.py --port 8080
```

> [!NOTE]
> Ctrl+C to quit

## Step 3: Create PostgreSQL local database

> [!WARNING]
> _If u haven't installed PostgreSQL visit [Download PostgreSQL](https://www.postgresql.org/download/) link and install_
> _for your system_

### Run script to make init_db.sql file initialize DB.

```
psql postgres -U postgres -h localhost -f init_db.sql
```