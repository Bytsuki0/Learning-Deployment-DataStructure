# 📚 Complete Learning Guide: Flask + HTML - Library Management System

**For Beginners Learning to Code**

This document explains how Flask and HTML work together in your Library Management application. We'll break down every concept step-by-step with real examples from your code.

---

## 📖 Table of Contents

1. [What is Flask?](#what-is-flask)
2. [What is HTML?](#what-is-html)
3. [How Flask and HTML Work Together](#how-flask-and-html-work-together)
4. [Project Architecture](#project-architecture)
5. [Step-by-Step Code Walkthrough](#step-by-step-code-walkthrough)
6. [Common Concepts Explained](#common-concepts-explained)
7. [How Data Flows Through Your App](#how-data-flows-through-your-app)
8. [Troubleshooting Guide](#troubleshooting-guide)

---

## What is Flask?

### 🤔 The Simple Answer

**Flask** is a Python web framework - a tool that helps you build web applications. Think of it as a traffic controller:
- It listens for when users visit different pages (URLs)
- It decides what to do based on which page they're visiting
- It sends back HTML pages or data to the user

### 📝 Real Analogy

Imagine a restaurant:
- **Customer** = Web browser (like Chrome, Firefox)
- **Waiter** = Flask (listens to requests)
- **Kitchen** = Your Python code (processes requests)
- **Meal** = The HTML page sent back to the browser

When a customer orders, the waiter takes the order to the kitchen, the kitchen prepares it, and the waiter brings it back.

### 🔍 What Flask Does in YOUR Project

In `app.py`, Flask does these things:

1. **Creates the app** - `app = Flask(__name__)`
2. **Listens for URL visits** - Uses `@app.route()` decorators
3. **Handles form submissions** - When users fill out and submit forms
4. **Fetches data from database** - Calls functions from `models.py`
5. **Sends HTML pages** - Uses `render_template()` to send HTML files

---

## What is HTML?

### 🤔 The Simple Answer

**HTML** (HyperText Markup Language) is the language used to create web pages. It's what you see when you open a website in your browser.

### 📝 Key Concepts

HTML uses **tags** - special labels that tell the browser how to display content:

```html
<!-- This is a comment - the browser ignores it -->

<h1>This is a heading (large text)</h1>
<p>This is a paragraph (normal text)</p>
<a href="/users">This is a link</a>
<button>Click me!</button>
<input type="text" name="cpf" placeholder="Enter CPF">
```

### 🏗️ Structure of HTML

Every HTML page has this basic structure:

```html
<!DOCTYPE html>           <!-- Tells browser this is HTML5 -->
<html>                    <!-- Start of HTML document -->
  <head>                  <!-- Info ABOUT the page (not shown to user) -->
    <title>Page Title</title>  <!-- Title shown in browser tab -->
    <link href="...">     <!-- Import CSS for styling -->
  </head>
  
  <body>                  <!-- Content SHOWN to the user -->
    <h1>Hello World!</h1>
    <p>This is visible on the page</p>
  </body>
</html>
```

### 📋 Common HTML Tags

| Tag | Purpose | Example |
|-----|---------|---------|
| `<h1>` - `<h6>` | Headings (h1 largest, h6 smallest) | `<h1>Title</h1>` |
| `<p>` | Paragraph of text | `<p>Some text</p>` |
| `<a>` | Link to another page | `<a href="/users">Go to Users</a>` |
| `<button>` | Clickable button | `<button>Click me</button>` |
| `<form>` | Container for input fields | `<form method="POST">...</form>` |
| `<input>` | Text field, checkbox, etc | `<input type="text" name="cpf">` |
| `<table>` | Organize data in rows/columns | `<table><tr><td>Data</td></tr></table>` |
| `<div>` | Container for grouping elements | `<div class="section">...</div>` |
| `<ul>` / `<li>` | Bulleted list | `<ul><li>Item 1</li></ul>` |

### 🎨 Bootstrap (CSS Framework)

Your project uses **Bootstrap** - a CSS library that makes pages look nice automatically.

```html
<!-- This line imports Bootstrap CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- Bootstrap classes make things look good -->
<h1 class="text-center mb-4">Bem-vindo à Biblioteca</h1>
```

Bootstrap classes do things like:
- `text-center` - Centers text
- `mb-4` - Adds space below (margin-bottom)
- `table-striped` - Makes table rows alternate colors
- `btn btn-primary` - Makes a styled button
- `container` - Adds a nice max-width and centering

---

## How Flask and HTML Work Together

### 🔄 The Request-Response Cycle

```
User → Browser → Flask → Database → Flask → HTML Template → Browser → User Sees Page
```

### Step-by-Step Example: Visiting the Home Page

1. **User types URL** → `http://localhost:5000/`
2. **Browser sends HTTP request** to Flask server
3. **Flask receives the request** and matches it to a route
4. **Flask runs the function** associated with that route
5. **Function gets data** (if needed from database)
6. **Flask renders HTML** - converts the template into final HTML
7. **Flask sends HTML** back to browser
8. **Browser displays** the HTML as a webpage

### 🎯 In Your Project: The Home Page

**In `app.py`:**
```python
@app.route('/')  # Listen for requests to the root URL (/)
def index():
    return render_template('index.html')  # Send back the index.html file
```

**In `templates/index.html`:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Biblioteca</title>
</head>
<body class="container mt-5">
    <h1 class="text-center mb-4">Bem-vindo à Biblioteca</h1>
    
    <div class="list-group">
        <a href="/emprestimos">Ver Empréstimos</a>
        <a href="/usuarios">Ver Usuários</a>
        <!-- ... more links ... -->
    </div>
</body>
</html>
```

**What happens:**
1. User visits `http://localhost:5000/`
2. Flask sees it matches the `/` route
3. Runs `index()` function
4. Returns the HTML from `index.html`
5. Browser displays the page with the menu

---

## Project Architecture

### 📁 File Structure Explained

```
your_project/
├── app.py              ← Main Flask application (the brain)
├── config.py           ← Configuration settings (database info)
├── models.py           ← Database functions (talks to MySQL)
├── requirements.txt    ← List of Python packages needed
├── templates/          ← Folder with HTML files
│   ├── index.html      ← Home page
│   ├── usuarios.html   ← List of users
│   ├── emprestimos.html ← List of loans
│   ├── cadastro_usuario.html   ← Form to add user
│   └── cadastro_emprestimo.html ← Form to add loan
└── LEARNING_GUIDE.md   ← This file!
```

### 🔗 How Files Connect

```
Browser requests /usuarios
        ↓
app.py @app.route('/usuarios')
        ↓
models.py get_all_usuarios()
        ↓
Database returns data
        ↓
app.py calls render_template('usuarios.html', usuarios=dados)
        ↓
usuarios.html loops through data with {% for %}
        ↓
Returns HTML to browser
```

---

## Step-by-Step Code Walkthrough

### 📝 Example 1: The Homepage (Simple Route)

**File:** `app.py`
```python
@app.route('/')  # ← This is a DECORATOR. It says "listen for /"
def index():
    # ↑ When someone visits /, this function runs
    
    return render_template('index.html')
    # ↑ Send back the HTML file located at templates/index.html
```

**What does `@app.route('/')`  mean?**
- `@` = This is a decorator (a special Python marker)
- `app.route` = Tell Flask to listen for a URL
- `/` = The root URL (homepage)

**What happens:**
- User visits `http://localhost:5000/`
- Flask sees this matches the `/` route
- Runs the `index()` function
- Function returns the HTML from `index.html`
- Browser displays the page

---

### 📝 Example 2: Displaying Data (GET Request)

**File:** `app.py`
```python
@app.route('/usuarios')  # ← Listen for /usuarios
def usuarios():
    dados = get_all_usuarios()  # ← Get all users from database
    # dados is now a list of dictionaries like:
    # [
    #   {'CPF': '123', 'Nome': 'João', 'Telefone': '1234'},
    #   {'CPF': '456', 'Nome': 'Maria', 'Telefone': '5678'}
    # ]
    
    return render_template('usuarios.html', usuarios=dados)
    # ↑ Pass the data to the template
```

**What does `render_template('usuarios.html', usuarios=dados)` mean?**
- `render_template()` = Convert HTML template to final HTML
- `'usuarios.html'` = The file name in the templates folder
- `usuarios=dados` = Pass variable `dados` to the template as `usuarios`

**In the template file `templates/usuarios.html`:**
```html
<table class="table table-striped table-bordered">
    <tbody>
        {% for usuario in usuarios %}  ← Jinja2 loop
        <tr>
            <td>{{ usuario['CPF'] }}</td>  ← Jinja2 variable
            <td>{{ usuario['Nome'] }}</td>
            <td>{{ usuario['Telefone'] }}</td>
        </tr>
        {% endfor %}
        </tbody>
</table>
```

**What does the template do?**
- `{% for usuario in usuarios %}` = Loop through each user in the list
- `{{ usuario['CPF'] }}` = Display the CPF value for this user
- `{% endfor %}` = End the loop
- This creates one `<tr>` row for each user

**Result:**
- 2 users in database = 2 rows in table
- 100 users in database = 100 rows in table

---

### 📝 Example 3: Handling Form Submission (POST Request)

**File:** `app.py`
```python
@app.route('/cadastro_usuario', methods=['GET', 'POST'])
#                                           ↑ Allow both GET and POST
def cadastro_usuario():
    if request.method == 'POST':
    #  ↑ Check if this is a form submission (not just visiting the page)
    
        # Get the form data from the user
        cpf = request.form['cpf']  ← Get the value from <input name="cpf">
        nome = request.form['nome']
        telefone = request.form['telefone']
        # ... more fields ...
        
        try:
            # Try to add to database
            adicionar_usuario(cpf, nome, telefone)
            flash('Usuário cadastrado com sucesso!')  ← Show success message
            return redirect(url_for('usuarios'))  ← Go to /usuarios page
        except Exception as e:
            # If error, show error message
            flash(f'Erro ao cadastrar usuário: {e}')
            return redirect(url_for('cadastro_usuario'))  ← Stay on form
    
    # If GET request (just visiting the page, not submitting)
    return render_template('cadastro_usuario.html')
```

**Key Concepts:**

1. **`methods=['GET', 'POST']`** - Accept both:
   - GET = Visiting the page normally
   - POST = Submitting a form

2. **`request.method == 'POST'`** - Check if form was submitted

3. **`request.form['cpf']`** - Get data from form field named "cpf"

4. **`flash()`** - Send message to user (shows in next page)

5. **`redirect()`** - Send user to different page

6. **`url_for()`** - Generate URL for a route by function name

**In the HTML form `templates/cadastro_usuario.html`:**
```html
<form method="POST" class="row g-3">
  <!-- method="POST" means send data to Flask when submitted -->
  
  <label class="form-label">CPF</label>
  <input type="text" class="form-control" 
         name="cpf" required>
  <!-- ↑ name="cpf" means this data will be received as request.form['cpf'] -->
  
  <label class="form-label">Nome</label>
  <input type="text" class="form-control" 
         name="nome" required>
  <!-- ↑ This becomes request.form['nome'] -->
  
  <button type="submit" class="btn btn-primary">Cadastrar</button>
  <!-- ↑ Clicking this submits the form to Flask -->
</form>
```

**What happens when user submits:**

1. User fills form:
   - CPF: 123456789
   - Nome: João
   - Telefone: 1234567
   
2. User clicks "Cadastrar" button

3. Browser sends POST request with form data

4. Flask receives in `request.form`:
   - `request.form['cpf']` = "123456789"
   - `request.form['nome']` = "João"
   - `request.form['telefone']` = "1234567"

5. Flask calls `adicionar_usuario()` to save to database

6. Flask shows success message with `flash()`

7. Flask redirects to `/usuarios` page

8. User sees updated list with new user

---

## Common Concepts Explained

### 🏷️ Decorators in Flask: `@app.route()`

A **decorator** is a Python feature that modifies a function.

```python
@app.route('/')  ← This is a decorator
def index():
    return "Hello!"
```

Think of it as a wrapper:
- Without the decorator: Just a regular function
- With the decorator: Flask knows this function should respond to HTTP requests

**Different routes:**
```python
@app.route('/')  # Homepage
def index():
    ...

@app.route('/usuarios')  # User list page
def usuarios():
    ...

@app.route('/cadastro_usuario')  # User registration page
def cadastro_usuario():
    ...

@app.route('/api/data')  # Can have any path
def api_data():
    ...
```

### 📤 HTTP Methods: GET vs POST

| Method | When Used | Data Visible | Safe |
|--------|-----------|--------------|------|
| **GET** | Request data / View page | In URL bar | Yes, read-only |
| **POST** | Submit form / Send data | Hidden, in body | Better for sensitive data |

**GET Example:**
```
User visits: http://localhost:5000/usuarios
Browser makes GET request
Flask returns list of users
```

**POST Example:**
```
User fills form and submits
Browser makes POST request with form data (hidden)
Flask saves to database
Flask redirects to another page
```

### 🔄 render_template() Explained

**`render_template(filename, var1=value1, var2=value2, ...)`**

This function:
1. Finds the HTML file in the `templates/` folder
2. Replaces Jinja2 variables with Python values
3. Returns the final HTML

**Example:**
```python
# In app.py
users_list = [
    {'name': 'João', 'age': 25},
    {'name': 'Maria', 'age': 30}
]

return render_template('users.html', users=users_list)
```

**In the HTML template:**
```html
<!-- Jinja2 loop -->
{% for user in users %}
    <p>{{ user['name'] }} - {{ user['age'] }} years old</p>
{% endfor %}

<!-- Output: -->
<!-- <p>João - 25 years old</p> -->
<!-- <p>Maria - 30 years old</p> -->
```

### 🎁 Jinja2 Template Language

Jinja2 is a templating language that lets you use Python in HTML.

**Variables:**
```html
<!-- Display a variable -->
<p>{{ name }}</p>
<p>{{ user['cpf'] }}</p>
<p>{{ data.field }}</p>
```

**If statements:**
```html
{% if user_count > 0 %}
    <p>There are {{ user_count }} users</p>
{% else %}
    <p>No users found</p>
{% endif %}
```

**For loops:**
```html
{% for item in items %}
    <p>{{ item['name'] }}</p>
{% endfor %}
```

**Filters:**
```html
<!-- uppercase filter -->
<p>{{ name|upper }}</p>

<!-- If name is "joão", displays: "JOÃO" -->
```

### 📨 request Object

The `request` object contains information about the HTTP request.

```python
from flask import request

# Get form data
cpf = request.form['cpf']  # From HTML <input name="cpf">
nome = request.form['nome']  # From HTML <input name="nome">

# Get URL parameters
page = request.args.get('page')  # From ?page=1

# Get request method
if request.method == 'POST':
    ...

# Get headers
user_agent = request.headers.get('User-Agent')

# Get request data
print(request.remote_addr)  # Client IP address
```

### 🔀 redirect() and url_for()

**`redirect(url)`** - Send user to a different page

```python
return redirect('/usuarios')  # Go to /usuarios page
return redirect('https://example.com')  # Go to external site
```

**`url_for(function_name, **kwargs)`** - Generate URL from function name

```python
# Instead of hardcoding URLs:
url_for('usuarios')  # Generates '/usuarios'
url_for('cadastro_usuario')  # Generates '/cadastro_usuario'

# In a redirect:
return redirect(url_for('usuarios'))
```

**Why use `url_for()`?**
- If you change the route, you don't need to update redirects
- Easier to maintain code
- Dynamic URL generation

### 💬 flash() Messages

**`flash(message)`** - Send a temporary message to user

```python
flash('User saved successfully!')
```

**In HTML template:**
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

Messages appear once, then disappear (stored in session).

---

## How Data Flows Through Your App

### 🔄 Complete Flow: Adding a New User

**Step 1: User visits the registration form**
```
Browser → GET /cadastro_usuario
          ↓
Flask receives GET request
          ↓
Runs: cadastro_usuario() function
          ↓
request.method == 'GET' (not POST)
          ↓
render_template('cadastro_usuario.html')
          ↓
Returns form HTML to browser
          ↓
Browser displays empty registration form
```

**Step 2: User fills form and submits**
```
User fills:
- CPF: 123456789
- Nome: João Silva
- Telefone: 1234567890
- Celular: 9876543210
- Endereco: Rua A, 123

User clicks "Cadastrar" button
          ↓
Browser sends POST /cadastro_usuario with form data
```

**Step 3: Flask processes the form**
```
Flask receives POST request
          ↓
Runs: cadastro_usuario() function (same function!)
          ↓
request.method == 'POST' (it's a form submission!)
          ↓
Extracts data:
- cpf = request.form['cpf'] = "123456789"
- nome = request.form['nome'] = "João Silva"
- telefone = request.form['telefone'] = "1234567890"
- celular = request.form['celular'] = "9876543210"
- endereco = request.form['endereco'] = "Rua A, 123"
```

**Step 4: Flask saves to database**
```
Calls: adicionar_usuario(cpf, rg, nome, telefone, celular, endereco)
          ↓
models.py adicionar_usuario() function runs
          ↓
Creates MySQL cursor
          ↓
Executes INSERT SQL:
INSERT INTO usuario (CPF, RG, Nome, Telefone, Celular, Endereco)
VALUES ('123456789', ..., 'João Silva', ...)
          ↓
Database confirms: User saved!
          ↓
Commits the transaction (saves permanently)
```

**Step 5: Flask shows success message**
```
flash('Usuário cadastrado com sucesso!')
          ↓
Message stored in session
```

**Step 6: Flask redirects to user list**
```
redirect(url_for('usuarios'))
          ↓
Browser receives: Go to /usuarios
          ↓
Browser makes new GET request to /usuarios
```

**Step 7: Flask displays updated list**
```
Runs: usuarios() function
          ↓
Calls: dados = get_all_usuarios()
          ↓
Database returns: SELECT * FROM usuario
          ↓
Gets all users INCLUDING the new one we just added!
          ↓
render_template('usuarios.html', usuarios=dados)
          ↓
Template loops through data:
{% for usuario in usuarios %}
    <tr>
        <td>123456789</td>  ← Our new user!
        <td>João Silva</td>
        ...
    </tr>
{% endfor %}
```

**Step 8: Browser shows updated page**
```
Browser displays table with all users
          ↓
Success message shown: "Usuário cadastrado com sucesso!"
          ↓
New user visible in the table
```

---

## HTML Form Deep Dive

### 📝 Form Elements

**Text Input:**
```html
<input type="text" name="cpf" placeholder="Enter CPF" required>
<!-- 
  - type="text" → Single line text
  - name="cpf" → In Flask: request.form['cpf']
  - placeholder → Gray hint text
  - required → User must fill this
-->
```

**Number Input:**
```html
<input type="number" name="idade" min="1" max="120">
<!-- 
  - type="number" → Only accepts numbers
  - min/max → Set boundaries
-->
```

**Date Input:**
```html
<input type="date" name="data_emprestimo">
<!-- 
  - type="date" → Shows calendar picker
  - Value format: YYYY-MM-DD
-->
```

**Select Dropdown:**
```html
<select name="categoria" required>
    <option value="">-- Choose --</option>
    <option value="ficção">Ficção</option>
    <option value="técnico">Técnico</option>
</select>
<!-- 
  - In Flask: request.form['categoria'] = selected value
  - First option with empty value is like "no selection"
-->
```

**Checkbox:**
```html
<input type="checkbox" name="notificacoes" value="sim">
Receber notificações
<!-- 
  - In Flask: request.form.get('notificacoes') = "sim" or None
-->
```

**Radio Button:**
```html
<input type="radio" name="tipo" value="usuario">
Usuário
<input type="radio" name="tipo" value="admin">
Administrador
<!-- 
  - In Flask: request.form['tipo'] = selected value
  - Only one can be selected
-->
```

**Button Types:**
```html
<!-- Submit button - sends form to Flask -->
<button type="submit" class="btn btn-primary">Cadastrar</button>

<!-- Reset button - clears all fields -->
<button type="reset" class="btn btn-secondary">Limpar</button>

<!-- Regular button - needs JavaScript to do something -->
<button type="button" class="btn btn-info">More Info</button>
```

### 🔗 Form Attributes

```html
<form method="POST" action="/cadastro_usuario" class="row g-3">
<!--
  - method="POST" → Send data in request body (safer)
  - action="/cadastro_usuario" → Where to send form data (optional, sends to same URL if omitted)
  - class="row g-3" → Bootstrap classes for styling
-->
```

**Method options:**
- `GET` → Data visible in URL (not secure for passwords)
- `POST` → Data hidden in request body (better for sensitive data)

---

## Tables Explained

### 📊 Creating a Dynamic Table

**In Flask (app.py):**
```python
@app.route('/emprestimos')
def emprestimos():
    dados = get_all_emprestimos()  # Gets list of loan records
    return render_template('emprestimos.html', emprestimos=dados)
```

**In HTML (templates/emprestimos.html):**
```html
<table class="table table-striped table-bordered">
    <!-- Table Header -->
    <thead class="table-dark">
        <tr>
            <th>Código</th>
            <th>Data Empréstimo</th>
            <th>Usuário</th>
            <th>Telefone</th>
        </tr>
    </thead>
    
    <!-- Table Body - Dynamic Rows -->
    <tbody>
        {% for emprestimo in emprestimos %}
        <tr>
            <td>{{ emprestimo['Codigo'] }}</td>
            <td>{{ emprestimo['Data_do_Emprestimo'] }}</td>
            <td>{{ emprestimo['Usuario_Nome'] }}</td>
            <td>{{ emprestimo['Usuario_Telefone'] }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

**How it works:**
1. Flask passes list of dictionaries to template
2. Template loops through each item
3. Each iteration creates a `<tr>` (table row)
4. Each `<td>` (table data) displays one field

**Bootstrap table classes:**
- `table-striped` → Alternate row colors
- `table-bordered` → Show borders
- `table-dark` → Dark background for header
- `table-hover` → Highlight row on mouse over

---

## Bootstrap CSS Framework

### 🎨 Why Use Bootstrap?

Bootstrap provides pre-made CSS classes that style elements beautifully without writing CSS code.

### 📐 Container & Grid

```html
<!-- Container centers content -->
<div class="container">
    <!-- Rows organize content -->
    <div class="row">
        <!-- Columns (12 columns total) -->
        <div class="col-md-6">
            <!-- Takes half the width on medium screens -->
            Left half
        </div>
        <div class="col-md-6">
            <!-- Takes half the width on medium screens -->
            Right half
        </div>
    </div>
</div>
```

### 🎯 Common Classes

**Spacing:**
- `mt-4` → Margin top (space above)
- `mb-4` → Margin bottom (space below)
- `p-3` → Padding (space inside)

**Text:**
- `text-center` → Center align text
- `text-end` → Right align text
- `text-primary` → Blue text color
- `text-danger` → Red text color

**Colors:**
- `bg-primary` → Blue background
- `bg-success` → Green background
- `bg-danger` → Red background

**Components:**
- `btn btn-primary` → Styled button
- `alert alert-success` → Success message box
- `list-group` → Styled list

---

## Troubleshooting Guide

### ❌ "Template Not Found"

**Error:** `jinja2.exceptions.TemplateNotFoundError`

**Possible causes:**
1. HTML file not in `templates/` folder
2. Wrong file name or spelling
3. Flask looking in wrong location

**Solution:**
```
Correct: templates/usuarios.html
Wrong: Users.html (not in templates folder)
Wrong: user.html (file is called usuarios.html)
```

### ❌ "KeyError" in Template

**Error:** `jinja2.exceptions.UndefinedError: 'usuarios' is undefined`

**Possible causes:**
1. Variable not passed to template
2. Wrong variable name

**Solution:**
```python
# app.py
return render_template('usuarios.html', usuarios=dados)
                                        ↑ Must match template

# usuarios.html
{% for user in usuarios %}  ← Must match variable name
```

### ❌ Form Data Not Received

**Problem:** `request.form` is empty

**Check:**
1. Form method is POST: `<form method="POST">`
2. Input has name attribute: `<input name="cpf">`
3. Button is type submit: `<button type="submit">`

**Solution:**
```html
<!-- Wrong -->
<input class="form-control">

<!-- Correct -->
<input class="form-control" name="cpf" required>
```

### ❌ Page Not Found

**Error:** `404 Not Found`

**Possible causes:**
1. Route doesn't exist
2. URL is misspelled
3. Flask server not running

**Solution:**
```python
# Make sure route exists
@app.route('/usuarios')  ← This URL exists
def usuarios():
    ...

# Not /users or /user - must match exactly
```

### ❌ Database Connection Error

**Error:** `Can't connect to MySQL server`

**Check:**
1. MySQL server is running
2. Credentials in `config.py` are correct
3. Database exists

**Solution:**
```python
# config.py - verify these settings
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3307
MYSQL_USER = "root"
MYSQL_PASSWORD = ""  # Set if you have one
MYSQL_DB = "biblioteca"
```

### ❌ Form Data Lost After Error

**Problem:** User submits form, gets error, data disappears

**Solution:** Keep form filled with submitted data:

```html
<!-- In the form -->
<input type="text" name="cpf" value="{{ request.form.get('cpf', '') }}">
<!--                                  ↑ Shows submitted value if there's an error -->
```

---

## Learning Path

### 🎯 Week 1: Foundations

1. **Flask Basics**
   - Read "What is Flask?" section
   - Understand @app.route() decorator
   - Run the app, visit each page
   
2. **HTML Basics**
   - Learn HTML tags (h1, p, a, button, etc)
   - Understand HTML structure
   - Look at index.html in editor

3. **Bootstrap**
   - Visit bootstrap.com to explore classes
   - Apply classes to elements
   - Change styling without writing CSS

### 🎯 Week 2: Templates & Data

1. **Jinja2 Templates**
   - Learn {% for %} loops
   - Learn {{ }} variables
   - Look at usuarios.html and emprestimos.html

2. **Passing Data**
   - Study render_template() in app.py
   - See how data flows from Flask to template
   - Add new fields to tables

3. **Tables**
   - Learn table structure (<table>, <tr>, <td>)
   - Create new table from data
   - Style with Bootstrap

### 🎯 Week 3: Forms

1. **Form Elements**
   - Learn <input>, <select>, <textarea>
   - Understand name attribute
   - Study cadastro_usuario.html

2. **Form Handling**
   - Learn GET vs POST
   - Study request.method
   - Study request.form[]

3. **Form Submission**
   - Follow complete flow in "Step-by-Step Code Walkthrough"
   - Trace data from HTML form to database
   - Add error handling with try/except

### 🎯 Week 4: Mini Projects

1. **Modify existing forms**
   - Add new field to usuario form
   - Update database model
   - Update Flask route

2. **Create new page**
   - Add new route in app.py
   - Create new HTML template
   - Style with Bootstrap

3. **Add validation**
   - Check if CPF is valid format
   - Check if email is valid
   - Show error messages

---

## Quick Reference

### Flask Code Template

```python
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Read page (GET)
@app.route('/page_name')
def page_name():
    data = get_data_from_somewhere()
    return render_template('page_name.html', variable_name=data)

# Submission page (GET and POST)
@app.route('/form_page', methods=['GET', 'POST'])
def form_page():
    if request.method == 'POST':
        # Process form
        field_value = request.form['field_name']
        try:
            save_to_database(field_value)
            flash('Success!')
            return redirect(url_for('page_name'))
        except Exception as e:
            flash(f'Error: {e}')
            return redirect(url_for('form_page'))
    return render_template('form_page.html')

if __name__ == '__main__':
    app.run(debug=True)
```

### HTML Form Template

```html
<!DOCTYPE html>
<html>
<head>
    <title>Page Title</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="container mt-4">
    <h1 class="mb-4">Form Title</h1>
    
    <!-- Flash messages -->
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul class="alert alert-info">
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    
    <!-- Form -->
    <form method="POST" class="row g-3">
        <div class="col-md-6">
            <label class="form-label">Field Name</label>
            <input type="text" class="form-control" name="field_name" required>
        </div>
        
        <div class="col-12">
            <button type="submit" class="btn btn-primary">Submit</button>
        </div>
    </form>
</body>
</html>
```

---

## Key Takeaways

✅ **Flask** listens for website visitors and decides what to show them

✅ **HTML** is the language that creates the web pages

✅ **Routes** (with @app.route) tell Flask which URL leads to which page

✅ **Templates** (with Jinja2) mix HTML with Python data

✅ **Forms** (with method="POST") collect data from users

✅ **request.form** accesses data submitted in HTML forms

✅ **render_template** converts templates to HTML pages

✅ **Bootstrap** makes pages look nice with CSS classes

✅ **Database** (MySQL) stores data permanently

✅ **Data flow** goes: User → Browser → Flask → Database → Flask → HTML → Browser → User Sees Page

---

## Additional Resources

**Official Documentation:**
- Flask: https://flask.palletsprojects.com/
- Jinja2: https://jinja.palletsprojects.com/
- Bootstrap: https://getbootstrap.com/docs/5.3/
- HTML: https://developer.mozilla.org/en-US/docs/Web/HTML/

**Video Tutorials:**
- Flask Mega-Tutorial by Miguel Grinberg
- Bootstrap Documentation Video Series
- HTML & CSS for Beginners

---

**Last Updated:** 2026-06-07
**For Questions:** Study the "How Data Flows Through Your App" section and trace the complete process
**Good Luck Learning! 📚**
