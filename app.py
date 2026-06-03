import os
from datetime import datetime
import pandas as pd
from functools import wraps
from flask import Flask, render_template, request, redirect, flash, send_file, session, url_for
from database import get_connection

app = Flask(__name__)
app.secret_key = "scrapk_secure_secret_key"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def dashboard():
    connection = get_connection()
    stats = {
        'total_vendors': 0,
        'smartphone_users': 0,
        'paper_collectors': 0,
        'plastic_collectors': 0,
        'metal_collectors': 0,
        'tech_collectors': 0
    }
    
    if connection:
        try:
            cursor = connection.cursor()
            
            # Total vendors count
            cursor.execute("SELECT COUNT(*) FROM vendors")
            stats['total_vendors'] = cursor.fetchone()[0]
            
            # Smartphone users count
            cursor.execute("SELECT COUNT(*) FROM vendors WHERE uses_smartphone = 1")
            stats['smartphone_users'] = cursor.fetchone()[0]
            
            cursor.close()
            connection.close()
        except Exception as e:
            print("Error retrieving dashboard statistics:", e)
            
    return render_template("dashboard.html", stats=stats)

@app.route("/vendors")
@login_required
def view_vendors():
    connection = get_connection()
    vendors = []
    
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM vendors ORDER BY id DESC")
            vendors = cursor.fetchall()
            cursor.close()
            connection.close()
        except Exception as e:
            print("Error fetching vendors list:", e)
            
    return render_template("view_vendors.html", vendors=vendors)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add_vendor():
    if request.method == "POST":
        print("FORM SUBMITTED ✅")
        print(request.form)

        full_name = request.form.get("full_name")
        business_name = request.form.get("business_name")
        mobile_no = request.form.get("mobile_no")
        email = request.form.get("email")
        full_address = request.form.get("full_address")
        working_area = request.form.get("working_area")
        
        experience_years = request.form.get("experience_years")
        if not experience_years or experience_years.strip() == "":
            experience_years = None
        else:
            try:
                experience_years = int(experience_years)
            except ValueError:
                experience_years = None

        uses_smartphone = int(request.form.get("uses_smartphone", 0))
        whatsapp_available = int(request.form.get("whatsapp_available", 0))
        interested_in_app = int(request.form.get("interested_in_app", 0))
        
        scrap_paper = 1 if request.form.get("scrap_paper") else 0
        scrap_plastic = 1 if request.form.get("scrap_plastic") else 0
        scrap_metal = 1 if request.form.get("scrap_metal") else 0
        scrap_electronics = 1 if request.form.get("scrap_electronics") else 0
        scrap_other = 1 if request.form.get("scrap_other") else 0

        connection = get_connection()
        print("DB CONNECTION:", connection)

        if connection:
            try:
                cursor = connection.cursor()

                query = """
                INSERT INTO vendors 
                (full_name, business_name, mobile_no, email, full_address, working_area,
                 experience_years, uses_smartphone, whatsapp_available, interested_in_app,
                 scrap_paper, scrap_plastic, scrap_metal, scrap_electronics, scrap_other)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                values = (
                    full_name,
                    business_name,
                    mobile_no,
                    email,
                    full_address,
                    working_area,
                    experience_years,
                    uses_smartphone,
                    whatsapp_available,
                    interested_in_app,
                    scrap_paper,
                    scrap_plastic,
                    scrap_metal,
                    scrap_electronics,
                    scrap_other
                )

                cursor.execute(query, values)
                connection.commit()
                print("DATA INSERTED ✅")
                cursor.close()
                connection.close()
                flash(f"Vendor '{full_name}' was successfully registered!", "success")
            except Exception as e:
                print("Error inserting vendor record:", e)
                flash(f"Failed to save vendor details: {str(e)}", "danger")
        else:
            flash("Database connection error! Could not connect to database server.", "danger")

        return redirect("/vendors")

    return render_template("add_vendors.html")

@app.route("/edit/<int:vendor_id>", methods=["GET", "POST"])
@login_required
def edit_vendor(vendor_id):
    connection = get_connection()
    if not connection:
        flash("Database connection error! Could not connect to database server.", "danger")
        return redirect("/vendors")

    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        full_name = request.form.get("full_name")
        business_name = request.form.get("business_name")
        mobile_no = request.form.get("mobile_no")
        email = request.form.get("email")
        full_address = request.form.get("full_address")
        working_area = request.form.get("working_area")
        
        experience_years = request.form.get("experience_years")
        if not experience_years or experience_years.strip() == "":
            experience_years = None
        else:
            try:
                experience_years = int(experience_years)
            except ValueError:
                experience_years = None

        uses_smartphone = int(request.form.get("uses_smartphone", 0))
        whatsapp_available = int(request.form.get("whatsapp_available", 0))
        interested_in_app = int(request.form.get("interested_in_app", 0))
        
        scrap_paper = 1 if request.form.get("scrap_paper") else 0
        scrap_plastic = 1 if request.form.get("scrap_plastic") else 0
        scrap_metal = 1 if request.form.get("scrap_metal") else 0
        scrap_electronics = 1 if request.form.get("scrap_electronics") else 0
        scrap_other = 1 if request.form.get("scrap_other") else 0

        try:
            query = """
            UPDATE vendors SET 
                full_name=%s, business_name=%s, mobile_no=%s, email=%s, 
                full_address=%s, working_area=%s, experience_years=%s, 
                uses_smartphone=%s, whatsapp_available=%s, interested_in_app=%s,
                scrap_paper=%s, scrap_plastic=%s, scrap_metal=%s, scrap_electronics=%s, scrap_other=%s
            WHERE id=%s
            """
            cursor.execute(query, (
                full_name, business_name, mobile_no, email, 
                full_address, working_area, experience_years, 
                uses_smartphone, whatsapp_available, interested_in_app,
                scrap_paper, scrap_plastic, scrap_metal, scrap_electronics, scrap_other,
                vendor_id
            ))
            connection.commit()
            flash(f"Vendor '{full_name}' was successfully updated!", "success")
        except Exception as e:
            print("Error updating vendor record:", e)
            flash(f"Failed to update vendor: {str(e)}", "danger")
        finally:
            cursor.close()
            connection.close()
            
        return redirect("/vendors")

    # GET request: load the vendor details
    cursor.execute("SELECT * FROM vendors WHERE id = %s", (vendor_id,))
    vendor = cursor.fetchone()
    cursor.close()
    connection.close()

    if not vendor:
        flash("Vendor profile not found!", "danger")
        return redirect("/vendors")

    return render_template("edit_vendor.html", vendor=vendor)

@app.route("/delete/<int:vendor_id>", methods=["POST"])
@login_required
def delete_vendor(vendor_id):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM vendors WHERE id = %s", (vendor_id,))
            connection.commit()
            cursor.close()
            connection.close()
            flash("Vendor was successfully deleted from directory.", "success")
        except Exception as e:
            print("Error deleting vendor:", e)
            flash(f"Failed to delete vendor: {str(e)}", "danger")
    else:
        flash("Database connection error! Could not connect to database server.", "danger")
        
    return redirect("/vendors")

@app.route("/export/<string:file_format>")
@login_required
def export_data(file_format):
    if file_format not in ['csv', 'xlsx']:
        flash("Invalid export format requested.", "danger")
        return redirect("/vendors")
        
    connection = get_connection()
    if not connection:
        flash("Database connection error! Export failed.", "danger")
        return redirect("/vendors")
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vendors ORDER BY id DESC")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        
        if not rows:
            flash("No vendor data found to export.", "warning")
            return redirect("/vendors")
            
        # Convert to pandas DataFrame
        df = pd.DataFrame(rows)
        
        # Mapped columns for printing
        column_mapping = {
            'id': 'ID',
            'full_name': 'Full Name',
            'business_name': 'Business / Shop Name',
            'mobile_no': 'Mobile Number',
            'email': 'Email Address',
            'full_address': 'Full Address',
            'working_area': 'Working / Collection Area',
            'experience_years': 'Experience (Years)',
            'scrap_paper': 'Collects Paper',
            'scrap_plastic': 'Collects Plastic',
            'scrap_metal': 'Collects Metal',
            'scrap_electronics': 'Collects E-Waste',
            'scrap_other': 'Collects Other',
            'uses_smartphone': 'Uses Smartphone',
            'whatsapp_available': 'WhatsApp Available',
            'interested_in_app': 'Interested in App',
            'created_at': 'Registration Date & Time'
        }
        
        # Filter and rename existing columns
        existing_cols = {col: name for col, name in column_mapping.items() if col in df.columns}
        df = df[list(existing_cols.keys())]
        df = df.rename(columns=existing_cols)
        
        # Format Boolean / TINYINT values for clarity
        yes_no_cols = [
            'Uses Smartphone', 'WhatsApp Available', 'Interested in App',
            'Collects Paper', 'Collects Plastic', 'Collects Metal', 
            'Collects E-Waste', 'Collects Other'
        ]
        for col in yes_no_cols:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: 'Yes' if x == 1 else 'No')
                
        # Ensure exports directory exists
        export_dir = 'exports'
        os.makedirs(export_dir, exist_ok=True)
        
        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vendors_export_{timestamp}.{file_format}"
        file_path = os.path.join(export_dir, filename)
        
        # Save file
        if file_format == 'csv':
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            mimetype = 'text/csv'
        else: # xlsx
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Vendors')
                
                # Style formatting: auto-adjust column width
                workbook = writer.book
                worksheet = writer.sheets['Vendors']
                for col in worksheet.columns:
                    max_len = max(len(str(cell.value or '')) for cell in col)
                    col_letter = col[0].column_letter
                    worksheet.column_dimensions[col_letter].width = max(max_len + 3, 10)
                    
            mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            
        flash(f"Data exported successfully to project exports folder as '{filename}'!", "success")
        
        return send_file(
            file_path,
            mimetype=mimetype,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        print("Export execution failed:", e)
        flash(f"Export failed: {str(e)}", "danger")
        return redirect("/vendors")


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

if __name__ == "__main__":
    app.run(debug=True)