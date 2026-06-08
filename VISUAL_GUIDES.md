# 📊 Flask & HTML - Visual Guides & Quick Reference

This file contains visual representations and quick reference sheets to complement the main learning guide.

---

## 🔄 Request-Response Cycle (Visual)

### Simple Example: Viewing Users Page

```
┌─────────────────────────────────────────────────────────────────┐
│                        WEB BROWSER                              │
│                                                                 │
│  User clicks link: "View Users"                                │
│  Browser makes: GET /usuarios                                  │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       │ HTTP Request
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│                        FLASK SERVER                             │
│                                                                 │
│  1. Receives: GET /usuarios                                    │
│  2. Matches route: @app.route('/usuarios')                     │
│  3. Runs function: usuarios()                                  │
│  4. Gets data: get_all_usuarios()                              │
│                                                                 │
│     ┌─────────────────────────┐                                │
│     │   MySQL Database        │                                │
│     │                         │                                │
│     │  SELECT * FROM usuario  │                                │
│     │  Returns: [users...]    │                                │
│     └─────────────────────────┘                                │
│                 ↓                                               │
│  5. Calls: render_template(                                    │
│       'usuarios.html',                                         │
│       usuarios=[users...]                                      │
│     )                                                          │
│  6. Jinja2 converts template to HTML                           │
│  7. Returns HTML to browser                                    │
│                                                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       │ HTTP Response (HTML)
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│                        WEB BROWSER                              │
│                                                                 │
│  Browser receives HTML:                                        │
│  <table>                                                       │
│    <tr><td>João</td><td>123456</td></tr>                       │
│    <tr><td>Maria</td><td>789012</td></tr>                      │
│  </table>                                                      │
│                                                                 │
│  Browser renders as: [Pretty table with users]                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### Complex Example: Submitting a Form

```
┌─────────────────────────────────────────────────────────────────┐
│                        WEB BROWSER                              │
│                                                                 │
│  User fills form:                                              │
│  - CPF: 12345678900                                            │
│  - Nome: João Silva                                            │
│  - Telefone: 1234567890                                        │
│                                                                 │
│  Clicks: "Cadastrar" button                                    │
│  <button type="submit">Cadastrar</button>                      │
│                                                                 │
│  Browser makes: POST /cadastro_usuario                         │
│  Data: cpf=12345678900&nome=João&telefone=1234567890          │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       │ HTTP POST Request (with form data)
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│                        FLASK SERVER                             │
│                                                                 │
│  1. Receives: POST /cadastro_usuario                           │
│  2. Matches route: @app.route(.../cadastro_usuario', ...)      │
│  3. Runs: cadastro_usuario()                                   │
│  4. Checks: if request.method == 'POST': ✓ YES                │
│  5. Extracts: request.form['cpf'] = "12345678900"             │
│               request.form['nome'] = "João Silva"              │
│               request.form['telefone'] = "1234567890"          │
│  6. Calls: adicionar_usuario(cpf, rg, nome, ...)              │
│                                                                 │
│     ┌─────────────────────────────────────────┐               │
│     │   MySQL Database                        │               │
│     │                                         │               │
│     │  INSERT INTO usuario (CPF, Nome, ...)   │               │
│     │  VALUES ("12345...", "João", ...)       │               │
│     │                                         │               │
│     │  Result: User saved! ✓                  │               │
│     └─────────────────────────────────────────┘               │
│                 ↓                                               │
│  7. Calls: flash('Success!')                                   │
│  8. Calls: redirect(url_for('usuarios'))                       │
│  9. Returns: Redirect response to /usuarios                    │
│                                                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       │ HTTP Response: Redirect to /usuarios
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│                        WEB BROWSER                              │
│                                                                 │
│  Browser sees: "Go to /usuarios"                               │
│  Browser makes: GET /usuarios (automatically)                  │
│                                                                 │
│  [Repeats first example above]                                │
│                                                                 │
│  Result:                                                       │
│  - User sees updated list                                      │
│  - New user "João Silva" is visible in table!                 │
│  - Success message shown at top                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ File Organization & Flow

```
your_project/
│
├── app.py
│   ├── Imports Flask and functions
│   ├── Creates Flask app
│   ├── Defines routes with @app.route()
│   │   ├── @app.route('/') → index()
│   │   ├── @app.route('/usuarios') → usuarios()
│   │   ├── @app.route('/cadastro_usuario', methods=['GET', 'POST']) → cadastro_usuario()
│   │   └── @app.route('/cadastro_emprestimo', methods=['GET', 'POST']) → cadastro_emprestimo()
│   │
│   └── Runs server: app.run(debug=True)
│
├── config.py
│   └── Database connection settings (unchanged)
│
├── models.py
│   ├── MySQL connection setup
│   ├── get_all_usuarios() - Queries database
│   ├── get_all_emprestimos() - Queries database
│   ├── adicionar_usuario() - Inserts data
│   └── adicionar_emprestimo() - Inserts data
│
└── templates/
    ├── index.html
    │   ├── Home page with menu
    │   └── Links to other pages
    │
    ├── usuarios.html
    │   ├── Receives: usuarios=[user objects]
    │   ├── Loops: {% for usuario in usuarios %}
    │   └── Displays: Table of all users
    │
    ├── emprestimos.html
    │   ├── Receives: emprestimos=[loan objects]
    │   ├── Loops: {% for emprestimo in emprestimos %}
    │   └── Displays: Table of all loans
    │
    ├── cadastro_usuario.html
    │   ├── Form with fields: cpf, rg, nome, telefone, celular, endereco
    │   ├── Submits to: POST /cadastro_usuario
    │   └── Gets data with: request.form['field_name']
    │
    └── cadastro_emprestimo.html
        ├── Form with fields: codigo, data_emprestimo, data_devolucao, etc
        ├── Submits to: POST /cadastro_emprestimo
        └── Gets data with: request.form['field_name']
```

---

## 🔍 Code Pattern Recognition

### Pattern 1: Display Data (Read Operation)

**When to use:** Show list of items from database

**Code structure:**
```python
@app.route('/page_name')
def page_name():
    data = get_all_items()  # Get from database
    return render_template('page_name.html', items=data)
```

**In template:**
```html
{% for item in items %}
    <div>{{ item['field'] }}</div>
{% endfor %}
```

**Your examples:**
- `/usuarios` → displays list
- `/emprestimos` → displays list

---

### Pattern 2: Display Form (GET)

**When to use:** Show empty form to user

**Code structure:**
```python
@app.route('/form_page', methods=['GET', 'POST'])
def form_page():
    if request.method == 'POST':
        # Handle submission
        pass
    
    # For GET request, show form
    return render_template('form_page.html')
```

**In template:**
```html
<form method="POST">
    <input type="text" name="field_name">
    <button type="submit">Send</button>
</form>
```

**Your examples:**
- `/cadastro_usuario` (when GET)
- `/cadastro_emprestimo` (when GET)

---

### Pattern 3: Handle Form Submission (POST)

**When to use:** Save data from form to database

**Code structure:**
```python
@app.route('/form_page', methods=['GET', 'POST'])
def form_page():
    if request.method == 'POST':  # ← Check if form submitted
        # Get data from form
        field_value = request.form['field_name']
        
        try:
            # Save to database
            save_function(field_value)
            flash('Success!')
            return redirect(url_for('success_page'))
        except Exception as e:
            flash(f'Error: {e}')
            return redirect(url_for('form_page'))
    
    return render_template('form_page.html')
```

**Your examples:**
- `/cadastro_usuario` (when POST)
- `/cadastro_emprestimo` (when POST)

---

## 📋 HTML Form Elements Cheat Sheet

```html
<!-- TEXT INPUTS -->
<input type="text" name="username">
<!-- In Flask: request.form['username'] -->

<!-- EMAIL INPUT -->
<input type="email" name="email">
<!-- Browser validates format automatically -->

<!-- PASSWORD INPUT -->
<input type="password" name="password">
<!-- Text hidden as dots -->

<!-- NUMBER INPUT -->
<input type="number" name="idade" min="0" max="150">
<!-- Only accepts numbers, has spinner buttons -->

<!-- DATE INPUT -->
<input type="date" name="data_nasc">
<!-- Shows calendar picker, value format: YYYY-MM-DD -->

<!-- TEXTAREA (Multiple lines) -->
<textarea name="descricao" rows="4" cols="50"></textarea>
<!-- For long text, can be resized -->

<!-- SELECT DROPDOWN -->
<select name="categoria">
    <option value="">-- Select --</option>
    <option value="fiction">Fiction</option>
    <option value="tech">Technical</option>
</select>
<!-- In Flask: request.form['categoria'] = selected value -->

<!-- CHECKBOX (can check multiple) -->
<input type="checkbox" name="opcoes" value="email">
Email
<input type="checkbox" name="opcoes" value="sms">
SMS
<!-- In Flask: request.form.getlist('opcoes') = [selected values] -->

<!-- RADIO (select one only) -->
<input type="radio" name="genero" value="M"> Male
<input type="radio" name="genero" value="F"> Female
<!-- In Flask: request.form['genero'] = selected value -->

<!-- HIDDEN INPUT (not visible to user) -->
<input type="hidden" name="user_id" value="123">
<!-- Still sent with form, useful for tracking -->

<!-- SUBMIT BUTTON -->
<button type="submit" class="btn btn-primary">Save</button>
<!-- Sends form to Flask -->

<!-- RESET BUTTON -->
<button type="reset" class="btn btn-secondary">Clear</button>
<!-- Clears all form fields -->
```

---

## 🎯 Jinja2 Template Cheat Sheet

```html
<!-- VARIABLES -->
{{ variable_name }}
{{ user['name'] }}
{{ user.name }}
{{ items|length }}

<!-- IF STATEMENT -->
{% if user_count > 0 %}
    <p>There are {{ user_count }} users</p>
{% elif user_count == 0 %}
    <p>No users</p>
{% endif %}

<!-- FOR LOOP -->
{% for item in items %}
    <li>{{ item['name'] }}</li>
{% endfor %}

<!-- FOR LOOP WITH INDEX -->
{% for item in items %}
    <p>{{ loop.index }}: {{ item['name'] }}</p>
    <!-- loop.index starts at 1 -->
    <!-- loop.index0 starts at 0 -->
{% endfor %}

<!-- FOR LOOP WITH CONDITIONAL -->
{% for item in items %}
    {% if item['active'] %}
        <p>{{ item['name'] }} is active</p>
    {% endif %}
{% endfor %}

<!-- EMPTY CHECK -->
{% if items %}
    <p>Items found</p>
{% else %}
    <p>No items</p>
{% endif %}

<!-- FILTERS -->
{{ text|upper }}            <!-- Uppercase -->
{{ text|lower }}            <!-- Lowercase -->
{{ text|capitalize }}       <!-- First letter capital -->
{{ items|length }}          <!-- Count items -->
{{ number|round(2) }}       <!-- Round to 2 decimals -->
{{ text|replace('a', 'b') }} <!-- Replace text -->

<!-- FLASH MESSAGES -->
{% with messages = get_flashed_messages() %}
    {% if messages %}
        <ul>
        {% for message in messages %}
            <li>{{ message }}</li>
        {% endfor %}
        </ul>
    {% endif %}
{% endwith %}
```

---

## 🐛 Common Mistakes & How to Fix Them

### Mistake 1: Wrong Variable Name

```python
# app.py
return render_template('users.html', users=data)  # Variable name is 'users'
```

```html
<!-- users.html - WRONG -->
{% for user in usuarios %}  <!-- Variable named 'usuarios' not 'users' -->
    {{ user['name'] }}
{% endfor %}

<!-- users.html - CORRECT -->
{% for user in users %}  <!-- Matches variable name from app.py -->
    {{ user['name'] }}
{% endfor %}
```

---

### Mistake 2: Accessing Dictionary Wrong

```python
# data = [{'name': 'João', 'age': 25}, {'name': 'Maria', 'age': 30}]
```

```html
<!-- WRONG -->
{{ user.name }}     <!-- Python objects use dot notation, dicts don't -->

<!-- CORRECT -->
{{ user['name'] }}  <!-- Dictionary access with brackets -->
```

---

### Mistake 3: Form Input Missing Name

```html
<!-- WRONG -->
<input type="text" class="form-control">
<!-- No name attribute, Flask can't access it -->

<!-- CORRECT -->
<input type="text" class="form-control" name="username">
<!-- Now in Flask: request.form['username'] works -->
```

---

### Mistake 4: Form Method Not POST

```html
<!-- WRONG -->
<form>  <!-- Default is GET, form data visible in URL -->
    <input type="password" name="password">
    <button type="submit">Login</button>
</form>

<!-- CORRECT -->
<form method="POST">  <!-- Data hidden in request body -->
    <input type="password" name="password">
    <button type="submit">Login</button>
</form>
```

---

### Mistake 5: Forgetting methods=['GET', 'POST']

```python
# WRONG - won't work for POST
@app.route('/form_page')
def form_page():
    if request.method == 'POST':  # Never true, only GET allowed
        ...

# CORRECT
@app.route('/form_page', methods=['GET', 'POST'])
def form_page():
    if request.method == 'POST':  # Now this works
        ...
```

---

### Mistake 6: Hardcoding URLs

```python
# WRONG - if route changes, this breaks
return redirect('/usuarios')

# CORRECT - generates URL from function name
return redirect(url_for('usuarios'))
```

---

### Mistake 7: Not Catching Database Errors

```python
# WRONG - error crashes the app
def handle_form():
    save_user(data)  # What if this fails?
    return "Success"

# CORRECT - handle errors gracefully
def handle_form():
    try:
        save_user(data)
        flash('Success!')
        return redirect(url_for('users'))
    except Exception as e:
        flash(f'Error: {e}')
        return redirect(url_for('form_page'))
```

---

## 📊 Data Type Conversion Reference

### When HTML Form Sends Data

```html
<input type="text" name="cpf">
<input type="number" name="age">
<input type="date" name="birth">
```

### In Flask, Everything is String

```python
cpf = request.form['cpf']          # "12345678900" (string)
age = request.form['age']          # "25" (string, not integer!)
birth = request.form['birth']      # "1998-05-15" (string)

# To convert:
age_int = int(request.form['age'])  # Now it's integer: 25
age_float = float(request.form['age'])  # Now it's float: 25.0

# Date handling (more complex)
from datetime import datetime
birth_date = datetime.strptime(request.form['birth'], '%Y-%m-%d')
```

---

## 🔐 Security Best Practices

### ✅ DO: Always Validate User Input

```python
# Always check input exists and is valid
if not request.form.get('cpf'):
    flash('CPF is required')
    return redirect(url_for('form'))

cpf = request.form['cpf'].strip()  # Remove whitespace
if len(cpf) != 11:
    flash('CPF must be 11 digits')
    return redirect(url_for('form'))
```

### ✅ DO: Use Parameterized Queries (your code does this!)

```python
# SECURE - your project uses this correctly
cur.execute("INSERT INTO usuario (CPF, Nome) VALUES (%s, %s)", (cpf, nome))

# INSECURE - Don't do this!
cur.execute(f"INSERT INTO usuario (CPF, Nome) VALUES ('{cpf}', '{nome}')")
# ↑ Vulnerable to SQL injection!
```

### ✅ DO: Use Flash for Messages

```python
# Good - message shown to user temporarily
flash('Successfully saved!')
```

### ❌ DON'T: Put Secret Keys in Code

```python
# WRONG - visible in code
app.secret_key = '153226@#'

# BETTER - use environment variable
import os
app.secret_key = os.getenv('SECRET_KEY', 'dev-key')
```

---

## 📱 Bootstrap Quick Classes

```html
<!-- LAYOUT -->
<div class="container">...</div>        <!-- Centered, max-width -->
<div class="row">...</div>              <!-- Flexible row -->
<div class="col-md-6">...</div>         <!-- Half width on medium+ screens -->

<!-- SPACING -->
mt-1, mt-2, mt-3, mt-4, mt-5           <!-- Margin Top (space above) -->
mb-1, mb-2, mb-3, mb-4, mb-5           <!-- Margin Bottom (space below) -->
p-1, p-2, p-3, p-4, p-5                <!-- Padding (space inside) -->

<!-- TEXT -->
text-center                             <!-- Center align -->
text-end                                <!-- Right align -->
text-muted                              <!-- Gray text -->
text-primary, text-danger, text-success <!-- Colored text -->

<!-- COLORS -->
bg-primary, bg-success, bg-danger       <!-- Background colors -->
text-primary, text-success, text-danger <!-- Text colors -->

<!-- TABLES -->
<table class="table">...</table>        <!-- Basic table -->
<table class="table table-striped">...  <!-- Alternating row colors -->
<table class="table table-bordered">... <!-- Show borders -->
<table class="table table-hover">...    <!-- Highlight on hover -->
<thead class="table-dark">...</thead>   <!-- Dark header -->

<!-- BUTTONS -->
<button class="btn btn-primary">...</button>      <!-- Blue -->
<button class="btn btn-success">...</button>      <!-- Green -->
<button class="btn btn-danger">...</button>       <!-- Red -->
<button class="btn btn-primary btn-lg">...</button> <!-- Large -->

<!-- ALERTS -->
<div class="alert alert-success">...</div>  <!-- Green alert -->
<div class="alert alert-danger">...</div>   <!-- Red alert -->
<div class="alert alert-info">...</div>     <!-- Blue alert -->

<!-- FORMS -->
<div class="mb-3">...</div>             <!-- Form group spacing -->
<input class="form-control">            <!-- Input styling -->
<label class="form-label">...</label>  <!-- Label styling -->
```

---

## 🧪 Testing Checklist

When you modify code, test these things:

### ✅ Route Testing
- [ ] Does URL exist and load without errors?
- [ ] Do links work correctly?
- [ ] Does back button work?

### ✅ Form Testing
- [ ] Can fill all fields in form?
- [ ] Does submit button work?
- [ ] Does validation work (required fields)?
- [ ] Does success message show?
- [ ] Does error message show (try invalid data)?

### ✅ Data Display Testing
- [ ] Do items display correctly in tables?
- [ ] Do all columns show data?
- [ ] Is table formatted nicely?
- [ ] Does sorting/filtering work (if added)?

### ✅ Database Testing
- [ ] Is new data saved after form submission?
- [ ] Does list update with new items?
- [ ] Are numbers correct?
- [ ] Can you see the data in MySQL?

### ✅ Bootstrap/Styling Testing
- [ ] Do buttons look good?
- [ ] Are forms properly spaced?
- [ ] Do tables have borders and styling?
- [ ] Is page responsive (looks good on small screens)?

---

## 🎓 Practice Exercises

### Exercise 1: Add a New Field
**Goal:** Add "email" field to user registration

**Steps:**
1. In database: Add EMAIL column to usuario table
2. In HTML: Add email input field in cadastro_usuario.html
3. In app.py: Add email to request.form extraction
4. In models.py: Add email parameter to INSERT query
5. Test: Register new user with email, verify it saves
6. Verify: Email appears in usuarios list

### Exercise 2: Create New Page
**Goal:** Create a page showing total users and loans

**Steps:**
1. In app.py: Create new route @app.route('/dashboard')
2. In app.py: Get count of users and loans
3. Create templates/dashboard.html
4. Display counts in HTML
5. Add link in index.html
6. Test: Click link, see dashboard

### Exercise 3: Add Validation
**Goal:** Validate CPF format before saving

**Steps:**
1. In app.py: Add validation before save
2. Check if CPF is 11 digits: if len(cpf) != 11: flash('Invalid CPF')
3. Test: Try saving with invalid CPF, should see error
4. Test: Try saving with valid CPF, should save

### Exercise 4: Add Edit Page
**Goal:** Edit an existing user

**Steps:**
1. In app.py: Create route @app.route('/edit_usuario/<cpf>')
2. In app.py: Get specific user by CPF
3. Create edit_usuario.html with form pre-filled with data
4. Handle POST to update database
5. Add Edit button in usuarios.html
6. Test: Edit user, verify changes saved

---

## 🔗 Important Links in Your Project

**These files work together:**

1. **index.html** - Starting point
   - Links to all other pages
   - Uses href="/usuarios", href="/cadastro_usuario"

2. **app.py** - Brain of app
   - Routes listen for URLs
   - Calls database functions
   - Renders templates

3. **models.py** - Database layer
   - Executes SQL queries
   - Returns data to app.py

4. **templates/*.html** - Frontend
   - Display pages to user
   - Contains forms
   - Uses Jinja2 for dynamic data

5. **config.py** - Settings
   - Database connection info

---

**Study Tips:**
1. Add comments to code explaining what each line does
2. Change one thing at a time and test
3. Use browser Developer Tools (F12) to see HTML
4. Use print() statements to debug
5. Read error messages carefully - they tell you the problem!

Good luck! 🚀
