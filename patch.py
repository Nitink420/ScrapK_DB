import os

def patch_app_py():
    with open("app.py", "r", encoding="utf-8") as f:
        content = f.read()

    # Imports
    if "from functools import wraps" not in content:
        content = content.replace("from flask import Flask, render_template, request, redirect, flash, send_file", 
                                  "from functools import wraps\nfrom flask import Flask, render_template, request, redirect, flash, send_file, session, url_for")

    # Add decorator definition right after secret key
    if "def login_required(f):" not in content:
        decorator_code = """
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
"""
        content = content.replace('app.secret_key = "scrapk_secure_secret_key"\n', 
                                  'app.secret_key = "scrapk_secure_secret_key"\n' + decorator_code)

    # Protect routes
    routes_to_protect = [
        '@app.route("/")',
        '@app.route("/vendors")',
        '@app.route("/add", methods=["GET", "POST"])',
        '@app.route("/edit/<int:vendor_id>", methods=["GET", "POST"])',
        '@app.route("/delete/<int:vendor_id>", methods=["POST"])',
        '@app.route("/export/<string:file_format>")'
    ]

    for route in routes_to_protect:
        if route in content and f"{route}\n@login_required" not in content:
            content = content.replace(route, f"{route}\n@login_required")

    # Add login and logout routes
    if "@app.route(\"/login\"" not in content:
        login_routes = """
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "admin123":
            session["logged_in"] = True
            flash("Logged in successfully!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))
"""
        content = content.replace("if __name__ == \"__main__\":", login_routes + "\nif __name__ == \"__main__\":")

    with open("app.py", "w", encoding="utf-8") as f:
        f.write(content)

def patch_templates():
    import glob
    for filepath in glob.glob("templates/*.html"):
        if filepath == "templates\\login.html" or filepath == "templates/login.html":
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        logout_item = """                <li class="nav-item">
                    <a href="/logout">
                        <span class="nav-icon">🚪</span>
                        <span>Logout</span>
                    </a>
                </li>
            </ul>"""
        
        if 'href="/logout"' not in content:
            content = content.replace('            </ul>', logout_item)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

if __name__ == "__main__":
    patch_app_py()
    patch_templates()
    print("Patching complete.")
