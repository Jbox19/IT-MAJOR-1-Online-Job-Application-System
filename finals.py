from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask_mysqldb import MySQL
import os

itmajor = Flask(__name__)
itmajor.secret_key = "super duper secret key"

itmajor.config["MYSQL_HOST"] = "localhost"
itmajor.config["MYSQL_USER"] = "root"
itmajor.config["MYSQL_PASSWORD"] = ""
itmajor.config["MYSQL_DB"] = "itmajor"

mysql = MySQL(itmajor)

@itmajor.route("/")
def main():
    return render_template("home.html")

@itmajor.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['uname']
        password = request.form['pword']

        cur = mysql.connection.cursor()
        cur.execute(f"SELECT username, password, user_type, firstname, lastname, email, file_name, file_name2 from tbl_approved WHERE username = '{username}'")
        record = cur.fetchone()
        cur.close()

        if record and password == record[1]:
            session['username'] = record[0]
            session['firstname'] = record[3]
            session['lastname'] = record[4]
            session['email'] = record[5]
            session['file_name'] = record[6]
            session['file_name2'] = record[7]
            user_type = record[2]

            if user_type == 'Applicant':
                return redirect(url_for('user_dashboard'))
            elif user_type == 'Employer':
                return redirect(url_for('employer'))
            else:
                return render_template("user_login.html", error="INVALID USER TYPE")

        else:
            return render_template("user_login.html", error="INVALID USERNAME OR PASSWORD")

    return render_template("user_login.html")
"""
@itmajor.route("/user_dashboard")
def user_dashboard():
    if "username" and "firstname" and "lastname" and "email" and "file_name" and "file_name2" in session:
        
        return render_template("user_dash.html", username=session["username"], firstname=session["firstname"], lastname=session["lastname"], email=session["email"], file_name=session["file_name"], file_name2=session["file_name2"])
    else:
        return render_template("main.html")
"""

@itmajor.route("/user_dashboard")
def user_dashboard():
    if "username" in session:
        username = session["username"]
        firstname = session["firstname"]
        lastname = session["lastname"]
        email = session["email"]
        file_name = session["file_name"]
        file_name2 = session["file_name2"]

        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT tbl_job.company_name, tbl_job.position, tbl_job.description, tbl_job.work_hour, tbl_job.salary,
                   tbl_job_interested.appointment_date, tbl_job_interested.appointment_time, tbl_job_interested.appointment_location, tbl_job_interested.appointment_status
            FROM tbl_job_interested
            JOIN tbl_job ON tbl_job_interested.job_id = tbl_job.job_id
            WHERE tbl_job_interested.email = %s
        """, (email,))
        applied_jobs = cur.fetchall()
        cur.close()

        return render_template("user_dash.html", 
                               username=username, 
                               firstname=firstname, 
                               lastname=lastname, 
                               email=email, 
                               file_name=file_name, 
                               file_name2=file_name2,
                               applied_jobs=applied_jobs)
    else:
        return render_template("main.html")


@itmajor.route("/available_jobs")
def available_jobs():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_job")
    data = cur.fetchall()
    mysql.connection.commit()
    cur.close()

    return render_template("available_jobs.html", data=data)

@itmajor.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('user_type', None)
    return redirect(url_for('login'))

@itmajor.route("/register", methods=["POST", "GET"])
def reg():
    if request.method == "POST":
        firstname = request.form['fname']
        lastname = request.form['lname']
        birthday = request.form['bday']
        gender = request.form['gend']
        address = request.form['add']
        email = request.form['email']
        user_type = request.form['type']
        username = request.form['uname']
        password = request.form['pword']
        file1 = request.files['file']
        file2 = request.files['file2']

        if file1 and file2:
            file_name1 = file1.filename
            file_name2 = file2.filename

            upload_dir = os.path.join(itmajor.root_path, "uploads")
            file_path1 = os.path.join(upload_dir, file_name1)
            file_path2 = os.path.join(upload_dir, file_name2)

            file1.save(file_path1)
            file2.save(file_path2)

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO tbl_registration (firstname, lastname, birthdate, gender, address, email, user_type, file_name, file_name2, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (firstname, lastname, birthday, gender, address, email, user_type, file_name1, file_name2, username, password))
            mysql.connection.commit()
            cur.close()

        return redirect(url_for("main"))
    else:
        return render_template("reg.html")

@itmajor.route("/view_file/<filename>")
def view_file(filename):
    upload_dir = os.path.join(itmajor.root_path, "uploads")
    return send_from_directory(upload_dir, filename)

@itmajor.route("/admin", methods = ["POST", "GET"])
def admin():
    if request.method == "POST":
        username = request.form['admin']
        password = request.form['pass']

        cur = mysql.connection.cursor()
        cur.execute(f"SELECT username, password from tbl_admin_acc WHERE username = '{username}'")
        admin = cur.fetchone()
        cur.close()
        
        if admin and password == admin[1]:
            session['username'] = admin[0]

            return redirect(url_for("admin_dash"))
        else:
            return render_template("admin.html", error = "INVALID USERNAME OR PASSWORD")

    return render_template("admin.html")

@itmajor.route("/admin_dashboard")
def admin_dash():
    if "username" in session:
        return render_template("admin_dashboard.html", username=session["username"])
    else:
        return render_template("admin.html")

@itmajor.route("/lagout")
def lagout():
    session.pop('username', None)

    return redirect(url_for("admin"))

@itmajor.route("/records", methods=["GET", "POST"])
def records():
    if request.method == "POST":
        reg_id = request.form.get("reg_id")
        new_status = request.form.get("status")

        if new_status == 'approve':
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO tbl_approved (firstname, lastname, email, user_type, file_name, file_name2, username, password) SELECT firstname, lastname, email, user_type, file_name, file_name2, username, password FROM tbl_registration WHERE reg_id = %s", (reg_id,))
            cur.execute("DELETE FROM tbl_registration WHERE reg_id = %s", (reg_id,))
            mysql.connection.commit()
            cur.close()
        elif new_status == 'reject':
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM tbl_registration where reg_id = %s", (reg_id,))
            mysql.connection.commit()
            cur.close()
        else:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE tbl_registration SET status = %s WHERE reg_id = %s", (new_status, reg_id))
            mysql.connection.commit()
            cur.close()

        return redirect(url_for("records"))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_registration")
    mysql.connection.commit()
    records = cur.fetchall()
    cur.close()

    return render_template("records.html", data=records)

@itmajor.route("/approved")
def approved():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_approved")
    mysql.connection.commit()
    approved = cur.fetchall()
    cur.close()

    return render_template("approved.html", approved=approved)

@itmajor.route("/employer_dashboard")
def employer():
    if "username" and "firstname" in session:
        employer_username = session["username"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tbl_job WHERE username = %s", (employer_username,))
        mysql.connection.commit()
        jobs = cur.fetchall()

        job_applicants = {}
        for job in jobs:
            cur.execute("SELECT tbl_job_interested.*, tbl_approved.* FROM tbl_job_interested JOIN tbl_approved ON tbl_job_interested.email = tbl_approved.email WHERE tbl_job_interested.job_id = %s", (job[0],))
            mysql.connection.commit()
            applicants = cur.fetchall()
            job_applicants[job[0]] = applicants

        cur.close()

        return render_template("employer_dashboard.html", username=session["username"], firstname=session["firstname"], jobs=jobs, job_applicants=job_applicants)
    else:
        return render_template("home.html")


@itmajor.route("/job")
def job():
    return render_template("job.html")

@itmajor.route("/create_job", methods=["GET", "POST"])
def create_job():
    if request.method == "POST":
        company_name = request.form['name']
        position = request.form['pos']
        description = request.form['des']
        work_hour = request.form['wh']
        salary = request.form['sal']

        if "username" in session:
            employer_username = session["username"]
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO tbl_job (username, company_name, position, description, work_hour, salary) VALUES (%s, %s, %s, %s, %s, %s)",
                        (employer_username, company_name, position, description, work_hour, salary))
            mysql.connection.commit()
            cur.close()

        return redirect(url_for("employer"))
    else:
        return render_template("job.html")
"""
@itmajor.route("/myjobs")
def myjobs():
    if "username" in session:
        employer_username = session["username"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tbl_job WHERE username = %s", (employer_username,))
        mysql.connection.commit()
        jobs = cur.fetchall()

        job_applicants = {}
        for job in jobs:
            cur.execute("SELECT tbl_job_interested.*, tbl_approved.* FROM tbl_job_interested JOIN tbl_approved ON tbl_job_interested.email = tbl_approved.email WHERE tbl_job_interested.job_id = %s", (job[0],))
            mysql.connection.commit()
            applicants = cur.fetchall()
            job_applicants[job] = applicants

        cur.close()

        return render_template("myjobs.html", username=session["username"], jobs=jobs, job_applicants=job_applicants)
    else:
        return render_template("home.html")
"""
@itmajor.route("/apply_job/<int:job_id>", methods=["POST"])
def apply_job(job_id):
    if request.method == "POST":
        if "username" in session:
            firstname = session["firstname"]
            lastname = session["lastname"]
            email = session["email"]
            file_name = session["file_name"]
            file_name2 = session["file_name2"]

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO tbl_job_interested (job_id, firstname, lastname, email, file_name, file_name2) VALUES (%s, %s, %s, %s, %s, %s)",
                        (job_id, firstname, lastname, email, file_name, file_name2))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for("user_dashboard"))
        else:
            return redirect(url_for("login"))
@itmajor.route("/appointment", methods=["POST"])
def appointment():
    job_id = request.form['job_id']
    return render_template("appointment.html", job_id=job_id, )

@itmajor.route("/create_appointment", methods=["POST"])
def create_appointment():
    job_id = request.form['job_id']
    date = request.form['date']
    time = request.form['time']
    location = request.form['location']

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE tbl_job_interested 
        SET appointment_date = %s, appointment_time = %s, appointment_location = %s, appointment_status = 'Confirmed'
        WHERE job_id = %s 
    """, (date, time, location, job_id, ))
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for("employer"))


if __name__ == "__main__":
    itmajor.run(debug=True)
