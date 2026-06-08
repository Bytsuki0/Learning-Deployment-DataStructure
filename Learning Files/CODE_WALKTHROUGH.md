# 💻 Code Walkthrough - Line by Line Explanations

This guide explains every line of your project code. Read this to understand exactly what each part does.

---

## 📄 File 1: app.py - The Main Application

### Imports Section

```python
from flask import Flask, render_template, request, redirect, url_for, flash
```

**Breaking it down:**

- `from flask import` - Import things FROM the Flask library
- `Flask` - The main class that creates a web application
- `render_template` - Function to convert HTML templates to web pages
- `request` - Object containing data about the HTTP request (forms, GET parameters, etc)
- `redirect` - Function to send user to a different page
- `url_for` - Function to generate URLs from function names
- `flash` - Function to show temporary messages to the user

**In English:** "From the Flask library, give me these tools: Flask to create an app, render_template to show HTML, request to get form data, redirect to move users around, url_for to generate links, and flash to show messages."

### More Imports

```python
from config import Config
```

**What it does:**
- Imports the `Config` class from config.py
- This contains database connection settings
- `Config` is a class (blueprint) with database info

### More Imports

```python
from models import mysql, get_all_emprestimos, get_all_usuarios, adicionar_usuario, adicionar_emprestimo
```

**What it does:**
- `mysql` - The MySQL database connection object
- `get_all_emprestimos` - Function to get all loans from database
- `get_all_usuarios` - Function to get all users from database
- `adicionar_usuario` - Function to add a new user
- `adicionar_emprestimo` - Function to add a new loan

**In English:** "From models.py, give me the database connection and these four functions."

### Creating the Flask App

```python
app = Flask(__name__)
```

**What it does:**
- Creates a new Flask application
- `Flask(__name__)` - Creates Flask app for this module
- `__name__` - Tells Flask "this is the main module"
- `app` - Variable that stores the application
- This is where all routes get registered

**In English:** "Create a new Flask web application called `app`."

### Configuration

```python
app.config.from_object(Config)
```

**What it does:**
- Tells Flask to use settings from the `Config` class
- `Config` contains database settings from config.py
- Now Flask knows how to connect to MySQL

**In English:** "Flask, use these database settings from the Config class."

### Secret Key

```python
app.secret_key = '153226@#'
```

**What it does:**
- Sets a secret key for the app
- This is used to encrypt session data (like flash messages)
- Keeps user sessions secure
- `'153226@#'` is the secret key value

**⚠️ Security Note:** This should be in an environment variable, not hardcoded!

**Better way:**
```python
import os
app.secret_key = os.getenv('SECRET_KEY', 'default-dev-key')
```

### Initialize MySQL

```python
mysql.init_app(app)
```

**What it does:**
- Takes the `mysql` object (from models.py)
- Initializes it with the Flask app
- Tells MySQL object which app to use
- Now MySQL can access app settings

**In English:** "MySQL, attach yourself to this Flask app and use its settings."

---

## 🛣️ Route 1: Homepage

```python
@app.route('/')
def index():
    return render_template('index.html')
```

### `@app.route('/')`

**What it does:**
- This is a **decorator** - modifies the function below it
- `app.route()` - Register this function as a route
- `'/'` - The URL path (root/homepage)
- Means: "When user visits http://localhost:5000/, run this function"

### `def index():`

**What it does:**
- `def` - Define a new function
- `index` - Function name (must match what you reference)
- This function runs when someone visits `/`

### `return render_template('index.html')`

**What it does:**
- `render_template()` - Convert HTML file to web page
- `'index.html'` - Look for file named index.html in templates/ folder
- `return` - Send the HTML back to browser
- Browser displays the HTML as a webpage

**Flow:**
1. User visits `/` 
2. Flask runs `index()` function
3. Function loads `index.html` from templates folder
4. Flask sends HTML to browser
5. Browser displays the homepage

---

## 🛣️ Route 2: View All Users

```python
@app.route('/usuarios')
def usuarios():
    dados = get_all_usuarios()
    return render_template('usuarios.html', usuarios=dados)
```

### Step by step:

**Line 1: `@app.route('/usuarios')`**
- Register route for URL `/usuarios`
- When user visits /usuarios, run the function below

**Line 2: `def usuarios():`**
- Define function called `usuarios`
- Note: function name matches route name (good practice, not required)

**Line 3: `dados = get_all_usuarios()`**
- `get_all_usuarios()` - Calls function from models.py
- This function queries database: `SELECT * FROM usuario`
- `dados` - Variable storing the result (list of users)
- Example: `dados = [{'CPF': '123', 'Nome': 'João'}, {'CPF': '456', 'Nome': 'Maria'}]`

**Line 4: `return render_template('usuarios.html', usuarios=dados)`**
- `render_template()` - Convert usuarios.html to HTML
- `'usuarios.html'` - The template file
- `usuarios=dados` - Pass the data to the template
  - Left side (`usuarios`) - Name of variable in template
  - Right side (`dados`) - Value from Python
  - In template, use: `{% for user in usuarios %}`

**Flow:**
1. User visits `/usuarios`
2. Flask runs `usuarios()` function
3. Function gets all users from database
4. Function passes them to template
5. Template loops through users and creates table rows
6. HTML sent to browser with all users

---

## 🛣️ Route 3: View All Loans

```python
@app.route('/emprestimos')
def emprestimos():
    dados = get_all_emprestimos()
    return render_template('emprestimos.html', emprestimos=dados)
```

**Same pattern as Route 2, but for loans:**
- Gets all loans from database
- Passes to emprestimos.html template
- Template displays table of loans

---

## 🛣️ Route 4: Register User (GET and POST)

```python
@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
```

### Understanding `methods=['GET', 'POST']`

**What it does:**
- Allow TWO types of requests on this route:
  - `GET` - User visits the page normally (show form)
  - `POST` - User submits the form (save data)
- Without this, route would only accept GET

### Get vs Post

| GET | POST |
|-----|------|
| User just visits the page | User submits form |
| Show the form | Process the form |
| No data from form | Form data hidden in request |

### The Function Body

```python
    if request.method == 'POST':
```

**What it does:**
- `if` statement - Check a condition
- `request.method` - What type of request is this?
- `== 'POST'` - Is it a POST request? (form submission)
- If TRUE: User submitted form, process it
- If FALSE: User just visiting, show form

### Extract Form Data

```python
        cpf = request.form['cpf']
        rg = request.form['rg']
        nome = request.form['nome']
        telefone = request.form['telefone']
        celular = request.form['celular']
        endereco = request.form['endereco']
```

**What it does:**
- `request.form` - Access data submitted in the form
- `['cpf']` - Get the value from input with name="cpf"
- `cpf = ...` - Store it in variable `cpf`

**Where does this data come from?**
- In HTML form: `<input name="cpf">`
- User types into field
- User clicks submit
- Form data sent to Flask
- We extract it with `request.form['cpf']`

### Try/Except Block

```python
        try:
            adicionar_usuario(cpf, rg, nome, telefone, celular, endereco)
            flash('Usuário cadastrado com sucesso!')
            return redirect(url_for('usuarios'))
        except Exception as e:
            flash(f'Erro ao cadastrar usuário: {e}')
            return redirect(url_for('cadastro_usuario'))
```

**What is `try/except`?**
- `try:` - Try to run this code
- If it works: Great!
- If error occurs: Go to `except:` block

**Why use it?**
- Database might fail
- Duplicate CPF
- Connection error
- We want to handle errors gracefully

### The Try Block

```python
            adicionar_usuario(cpf, rg, nome, telefone, celular, endereco)
```
- Call function from models.py
- Save user to database

```python
            flash('Usuário cadastrado com sucesso!')
```
- If save worked, show success message
- `flash()` stores message in session
- Message shows on next page

```python
            return redirect(url_for('usuarios'))
```
- Send user to /usuarios page
- Shows updated list with new user
- User sees: Success message + New user in table

### The Except Block

```python
        except Exception as e:
            flash(f'Erro ao cadastrar usuário: {e}')
            return redirect(url_for('cadastro_usuario'))
```

- `Exception as e` - Catch any error, store in variable `e`
- `flash(f'Erro ao cadastrar usuário: {e}')` - Show error message
  - `f'...'` - f-string, allows variables inside string
  - `{e}` - The error message
- `return redirect(url_for('cadastro_usuario'))` - Go back to form
- User stays on form page to try again

### Handle GET Request

```python
    return render_template('cadastro_usuario.html')
```

- When `request.method == 'POST'` is FALSE (user just visiting)
- Show empty form
- User fills it out
- Submits
- POST request received
- Cycle repeats

**Complete Flow:**

**Visit:**
1. User goes to `/cadastro_usuario`
2. `request.method == 'POST'` → FALSE
3. Render empty form
4. Show HTML to browser

**Submit:**
1. User fills form, clicks submit
2. Browser sends POST request
3. `request.method == 'POST'` → TRUE
4. Extract form data
5. Try to save
6. If success: Show message + redirect to list
7. If error: Show error + redirect back to form

---

## 🛣️ Route 5: Register Loan

```python
@app.route('/cadastro_emprestimo', methods=['GET', 'POST'])
def cadastro_emprestimo():
    if request.method == 'POST':
        fk_usuario_cpf = request.form['fk_usuario_cpf']
        fk_usuario_rg = request.form['fk_usuario_rg']
        data_do_emprestimo = request.form['data_do_emprestimo']
        data_da_devolucao = request.form['data_da_devolucao']
        quantidade_de_livros = request.form['quantidade_de_livros']
        codigo = request.form['codigo']
        try:
            adicionar_emprestimo(codigo, data_do_emprestimo, data_da_devolucao,
                                 quantidade_de_livros,
                                 fk_usuario_cpf, fk_usuario_rg)
            flash('Empréstimo cadastrado com sucesso!')
            return redirect(url_for('emprestimos'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Erro ao cadastrar empréstimo: {e}')
            return redirect(url_for('cadastro_emprestimo'))
    return render_template('cadastro_emprestimo.html', usuarios=get_all_usuarios())
```

**Same pattern as user registration, but note:**

### `mysql.connection.rollback()`

**What it does:**
- If error occurs, undo any partial changes
- Prevents broken data in database
- `rollback()` cancels the transaction

**Why important:**
- User saves partially valid data
- Error occurs
- Without rollback: Partial bad data stays in database
- With rollback: Everything cancelled, database clean

### Last Line - Pass Users to Template

```python
    return render_template('cadastro_emprestimo.html', usuarios=get_all_usuarios())
```

- When GET request (showing form)
- Also pass all users: `usuarios=get_all_usuarios()`
- Why? Form has dropdown to select which user
- Need list of users to populate dropdown

### Ending

```python
if __name__ == '__main__':
    app.run(debug=True)
```

**What it does:**
- `if __name__ == '__main__':` - Check if this file is being run directly
- `app.run(debug=True)` - Start Flask server
  - `debug=True` - Auto-reload on code changes, show detailed errors

**In English:** "If this file is run directly (not imported), start the Flask server in debug mode."

---

## 📄 File 2: config.py - Configuration

```python
class Config:
    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3307
    MYSQL_USER = "root"
    MYSQL_PASSWORD = ""
    MYSQL_DB = "biblioteca"
    MYSQL_CURSORCLASS = "DictCursor"
```

### What is this?

A **class** that stores all configuration in one place.

### Each Setting:

**`MYSQL_HOST = "127.0.0.1"`**
- Where is MySQL server?
- `127.0.0.1` is localhost (your computer)
- Change if MySQL on different computer

**`MYSQL_PORT = 3307`**
- Which port for MySQL?
- Default is 3306, yours uses 3307

**`MYSQL_USER = "root"`**
- Username to connect to MySQL
- `root` is default admin user

**`MYSQL_PASSWORD = ""`**
- Password for MySQL
- Empty (`""`) means no password
- Set if MySQL requires password

**`MYSQL_DB = "biblioteca"`**
- Which database to use?
- Must be created in MySQL first

**`MYSQL_CURSORCLASS = "DictCursor"`**
- How to receive data from MySQL?
- `DictCursor` returns data as dictionaries
- Example: `{'CPF': '123', 'Nome': 'João'}`
- Instead of tuples: `('123', 'João')`

### Why Use a Config Class?

✅ **Good practices:**
- Settings in one place
- Easy to change
- Can have different configs for dev/production
- Keep secrets organized

---

## 📄 File 3: models.py - Database Layer

### Imports

```python
from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor
```

**`from flask_mysqldb import MySQL`**
- Get MySQL connector for Flask
- `MySQL` - Class for database connection

**`from MySQLdb.cursors import DictCursor`**
- Get DictCursor for returning dictionaries
- Imported but not directly used (used in config)

### Create MySQL Object

```python
mysql = MySQL()
```

- Create MySQL object
- Later will be initialized with app in app.py
- `mysql.init_app(app)` in app.py connects it

### Function 1: Get All Users

```python
def get_all_usuarios():
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM usuario")
    result = cur.fetchall()
    cur.close()
    return result
```

**Line by line:**

**`cur = mysql.connection.cursor(DictCursor)`**
- Create a cursor (query tool)
- `mysql.connection` - The database connection
- `.cursor(DictCursor)` - Return results as dictionaries
- `cur` - Store cursor in variable

**`cur.execute("SELECT * FROM usuario")`**
- Send SQL query to database
- `SELECT * FROM usuario` - Get all users
- Database executes this query

**`result = cur.fetchall()`**
- Get all results from query
- `fetchall()` - Return as list of dictionaries
- Example: `[{'CPF': '123', 'Nome': 'João'}, {...}]`

**`cur.close()`**
- Close the cursor
- Free up resources
- Good practice

**`return result`**
- Send results back to caller
- In app.py: `dados = get_all_usuarios()`

---

### Function 2: Get All Loans

```python
def get_all_emprestimos():
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT
            e.Codigo,
            e.Data_do_Emprestimo,
            e.Data_da_Devolucao,
            e.FK_Usuario_CPF,
            e.FK_Usuario_RG,
            u.Nome AS Usuario_Nome,
            u.Telefone AS Usuario_Telefone,
            u.Celular AS Usuario_Celular,
            u.Endereco AS Usuario_Endereco
        FROM emprestimo e
        INNER JOIN usuario u
            ON e.FK_Usuario_CPF = u.CPF
           AND e.FK_Usuario_RG = u.RG
        ORDER BY e.Codigo DESC
    """)
    result = cur.fetchall()
    cur.close()
    return result
```

**What's different from get_all_usuarios()?**

**More complex SQL query:**
- `FROM emprestimo e` - Get from loan table
- `INNER JOIN usuario u` - Also get user data
- `ON e.FK_Usuario_CPF = u.CPF AND e.FK_Usuario_RG = u.RG` - Match by CPF and RG
- `AS Usuario_Nome` - Rename column in result
- `ORDER BY e.Codigo DESC` - Sort by code, newest first

**Why this complexity?**
- Need loan data AND user data
- `emprestimo` table has user IDs (foreign keys)
- `usuario` table has user details
- JOIN combines data from both tables

**Result example:**
```python
{
    'Codigo': '001',
    'Data_do_Emprestimo': '2024-01-15',
    'Usuario_Nome': 'João',
    'Usuario_Telefone': '1234567890',
    ...
}
```

---

### Function 3: Add User

```python
def adicionar_usuario(cpf, rg, nome, telefone, celular, endereco):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO usuario (CPF, RG, Nome, Telefone, Celular, Endereco)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (cpf, rg, nome, telefone, celular, endereco))
    mysql.connection.commit()
    cur.close()
```

**Parameters:**
- `cpf, rg, nome, telefone, celular, endereco` - Data to insert

**`cur.execute(..., (values))`**
- Send INSERT query with parameters
- `%s` - Placeholder for safe value insertion
- `(cpf, rg, nome, ...)` - Values to insert
- This prevents SQL injection attacks

**`mysql.connection.commit()`**
- Save changes to database
- Without commit: changes not permanent
- With commit: changes locked in database

**`cur.close()`**
- Close cursor, free resources

---

### Function 4: Add Loan

```python
def adicionar_emprestimo(codigo, data_do_emprestimo, data_da_devolucao,
                         quantidade_de_livros,
                         fk_usuario_cpf, fk_usuario_rg):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO emprestimo
        (Codigo, Data_do_Emprestimo, Data_da_Devolucao, Quantidade_de_Livros,
         FK_Usuario_CPF, FK_Usuario_RG)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        codigo,
        data_do_emprestimo,
        data_da_devolucao,
        quantidade_de_livros,
        fk_usuario_cpf,
        fk_usuario_rg
    ))
    mysql.connection.commit()
    cur.close()
```

**Same pattern as adicionar_usuario():**
- Create cursor
- Execute INSERT query with parameters
- Commit changes
- Close cursor

---

## 📄 Template File: usuarios.html

### Comments at Top

```html
<!-- 
    Página: usuarios.html
    Função: Exibe a lista de usuários cadastrados na biblioteca.
    ...
-->
```

**What this is:**
- HTML comment (browser ignores it)
- Explains what the file does
- Helps future programmers understand

### HTML Structure

```html
<!DOCTYPE html>
<html>
<head>
    <title>Usuários</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="container mt-4">
```

**`<!DOCTYPE html>`**
- Tells browser this is HTML5
- Required for all HTML files

**`<head>...</head>`**
- Information ABOUT page (not displayed to user)
- Contains title, stylesheets, scripts

**`<title>Usuários</title>`**
- Text shown in browser tab

**`<link ... bootstrap>`**
- Import Bootstrap CSS
- Makes page look nice automatically

**`<body class="container mt-4">`**
- Content displayed to user
- `class="container mt-4"` - Bootstrap classes
  - `container` - Centered, nice width
  - `mt-4` - Margin top (space above)

### Page Title

```html
    <h1 class="mb-4">Lista de Usuários</h1>
```

- `<h1>` - Large heading
- `class="mb-4"` - Bootstrap spacing class
- `mb-4` - Margin bottom (space below heading)

### Table Structure

```html
    <table class="table table-striped table-bordered">
        <thead class="table-dark">
            <tr>
                <th>CPF</th>
                <th>RG</th>
                <!-- ... more columns ... -->
            </tr>
        </thead>
```

**`<table>`** - Container for table

**`<thead>`** - Table header section
- `class="table-dark"` - Dark background

**`<tr>`** - Table row

**`<th>`** - Table header cell
- Shows column names

### Dynamic Table Body

```html
        <tbody>
            {% for usuario in usuarios %}
            <tr>
                <td>{{ usuario['CPF'] }}</td>
                <td>{{ usuario['RG'] }}</td>
                <!-- ... more columns ... -->
            </tr>
            {% endfor %}
        </tbody>
```

**`<tbody>`** - Table body section (data rows)

**`{% for usuario in usuarios %}`**
- Jinja2 loop
- Loop through each user in the `usuarios` list
- `usuarios` passed from app.py

**`<td>{{ usuario['CPF'] }}</td>`**
- `<td>` - Table data cell
- `{{ usuario['CPF'] }}` - Display CPF value
- `usuario` - Current user in loop
- `['CPF']` - Dictionary access to get CPF field

**`{% endfor %}`**
- End of loop

### How It Works

**In app.py:**
```python
dados = [
    {'CPF': '123', 'RG': '456', 'Nome': 'João'},
    {'CPF': '789', 'RG': '012', 'Nome': 'Maria'}
]
return render_template('usuarios.html', usuarios=dados)
```

**In template:**
```html
{% for usuario in usuarios %}
<tr>
    <td>{{ usuario['CPF'] }}</td>
</tr>
{% endfor %}
```

**Output HTML:**
```html
<tr>
    <td>123</td>
</tr>
<tr>
    <td>789</td>
</tr>
```

**Browser displays:** Table with 2 rows, CPFs 123 and 789

---

## 📄 Template File: cadastro_usuario.html

### Form Container

```html
<form method="POST" class="row g-3">
```

**`<form>`** - Container for input fields

**`method="POST"`**
- Send form data as POST request
- Data hidden in request body
- Safe for sensitive data

**`class="row g-3"`**
- Bootstrap classes
- `row` - Organize as row
- `g-3` - Gap/spacing between items

### Form Fields

```html
    <div class="col-md-6">
        <label class="form-label">CPF</label>
        <input type="text" class="form-control" name="cpf" required>
    </div>
```

**`<div class="col-md-6">`**
- Container for field
- `col-md-6` - Half width on medium screens

**`<label>`**
- Text above input field
- `class="form-label"` - Bootstrap styling

**`<input>`**
- Input field where user types
- `type="text"` - Single line text input
- `name="cpf"` - Field name
  - In Flask: `request.form['cpf']`
- `required` - User must fill this field
- `class="form-control"` - Bootstrap styling (nice appearance)

### Submit Button

```html
    <div class="col-12">
        <button type="submit" class="btn btn-primary">Cadastrar</button>
    </div>
```

**`<button type="submit">`**
- Button that submits form
- When clicked: sends POST request to Flask

**`class="btn btn-primary"`**
- Bootstrap classes
- `btn` - Button styling
- `btn-primary` - Blue color

**`</form>`**
- Closes form
- All inputs above are part of form

### Flash Messages in Form

```html
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul class="alert alert-info">
      {% for message in messages %}
        <li>{{ message }}</li>
      {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
```

**`{% with messages = get_flashed_messages() %}`**
- Get all messages that were flashed
- Store in `messages` variable

**`{% if messages %}`**
- If there are any messages

**`<ul>` and `<li>`**
- Unordered list
- Each message is list item

**`{{ message }}`**
- Display each message

**`class="alert alert-info"`**
- Bootstrap alert styling
- Blue colored box for messages

**Example:**
- Flask does: `flash('User saved!')`
- Message stored in session
- Next page shows message
- After page loads, message disappears

---

## 🔗 How Everything Connects

### The Complete Data Flow

**User registers new user:**

```
1. Browser shows form (from index.html)
   └─ User clicks "Cadastrar Usuário"

2. Browser loads /cadastro_usuario
   └─ app.py receives GET request
   └─ request.method == 'POST' → FALSE
   └─ Renders cadastro_usuario.html
   └─ Browser shows empty form

3. User fills form:
   - CPF: 12345678900
   - Nome: João Silva
   - etc

4. User clicks "Cadastrar" button
   └─ Form submits to /cadastro_usuario
   └─ Browser sends POST request
   └─ Form data included in request

5. app.py receives POST request
   └─ request.method == 'POST' → TRUE
   └─ Extracts: cpf = request.form['cpf'] = "12345678900"
   └─ Extracts: nome = request.form['nome'] = "João Silva"

6. app.py tries to save
   └─ Calls: adicionar_usuario(cpf, rg, nome, ...)
   └─ models.py receives call
   └─ Creates cursor
   └─ Executes: INSERT INTO usuario VALUES (...)
   └─ Commits transaction
   └─ Cursor closes

7. If success:
   └─ app.py: flash('Usuário cadastrado com sucesso!')
   └─ app.py: redirect(url_for('usuarios'))
   └─ Browser: Redirected to /usuarios

8. Browser makes GET /usuarios
   └─ app.py: runs usuarios()
   └─ Calls: get_all_usuarios()
   └─ models.py: SELECT * FROM usuario
   └─ Database returns all users (including new one!)
   └─ app.py: render_template('usuarios.html', usuarios=dados)
   └─ Template creates table with all users

9. Browser displays:
   └─ Success message at top
   └─ Table with all users
   └─ New user "João Silva" visible!

10. Success! 🎉
```

---

## 🐛 Debug Tips

### See What Data Is Being Sent

```python
# In app.py, add this:
@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        print("Form data received:")
        print(request.form)  # ← Shows all form data
        
        # Will show in terminal:
        # ImmutableMultiDict([('cpf', '12345678900'), ('nome', 'João'), ...])
```

### See What Data Is In Database

```python
# In app.py, add this:
@app.route('/usuarios')
def usuarios():
    dados = get_all_usuarios()
    print("Users from database:")
    print(dados)  # ← Shows what database returned
    return render_template('usuarios.html', usuarios=dados)
```

### See Template Variables

```html
<!-- In template, add this to see what data is being passed -->
<p>DEBUG: {{ usuarios }}</p>

<!-- Shows:
[{'CPF': '123', 'Nome': 'João'}, {'CPF': '456', 'Nome': 'Maria'}]
-->
```

---

## 📚 Key Terms Glossary

| Term | Meaning |
|------|---------|
| **Route** | URL pattern that Flask listens for |
| **Decorator** | `@` symbol, modifies function behavior |
| **Render** | Convert template to HTML |
| **Template** | HTML file with Jinja2 code |
| **Cursor** | Tool for executing database queries |
| **Commit** | Save changes to database |
| **Rollback** | Undo database changes |
| **GET** | Request data from server |
| **POST** | Send data to server |
| **Flash** | Temporary message to user |
| **Redirect** | Send user to different page |
| **URL** | Web address (example.com/page) |
| **HTTP** | Protocol for web communication |
| **Form** | HTML element for user input |
| **Input** | Field where user types text |
| **Button** | Clickable element |

---

**Study this section by:**
1. Read a function completely
2. Look at the code
3. See how it's used in app.py
4. Trace a complete data flow
5. Add print statements to debug
6. Modify slightly and test

Happy Learning! 🚀
