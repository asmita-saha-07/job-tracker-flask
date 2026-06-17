from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///job.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Job(db.Model):
    slno=db.Column(db.Integer, primary_key=True)
    company=db.Column(db.String(100), nullable=False)
    role=db.Column(db.String(100), nullable=False)
    notes=db.Column(db.String(700))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="Applied")

    def __repr__(self):
        return f"{self.slno} - {self.company} - {self.role}"

@app.route("/",methods=["GET","POST"])
def home():
    if request.method=="POST":
        company=request.form["company"]
        role=request.form["role"]
        notes=request.form["notes"]
        if company == "" or role == "":
            return redirect("/")
        position=Job(company=company, role=role, notes=notes)
        db.session.add(position)
        db.session.commit()
        return redirect("/")

    Alljobs=Job.query.all()
    return render_template("home.html", Alljobs=Alljobs)


@app.route("/update_status/<int:slno>/<string:status>", methods=["GET","POST"])
def update_status(slno, status):
    if request.method == "GET":
        job=Job.query.filter_by(slno=slno).first()
        job.status=status
        db.session.commit()
    return redirect("/")


@app.route("/delete/<int:slno>",methods=["GET","POST"])
def delete(slno):
    job=Job.query.filter_by(slno=slno).first()
    db.session.delete(job)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:slno>",methods=["GET","POST"])
def update(slno):
    job=Job.query.filter_by(slno=slno).first()
    if request.method=="POST":
        job.company=request.form["company"]
        job.role=request.form["role"]
        job.notes=request.form["notes"]
        if job.company == "" or job.role == "":
           return redirect("/")
        db.session.commit()
        return redirect("/")
    return render_template("update.html", job=job)
        


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)