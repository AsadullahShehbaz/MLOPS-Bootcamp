# Jinja 2 Expression
# Loop 

from flask import Flask,render_template,request,redirect,url_for

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html") 

@app.route("/success/<int:score>")
def success(score):
    result = ""
    if score >=50:
        result="passed"
    else:
        result="failed"

    
    return render_template("result.html",results=result) 

@app.route("/successif/<int:score>")
def successif(score):
    return render_template("index.html",results=score)


@app.route("/submit",methods=["GET","POST"])
def submit():
    total_score=0
    if request.method == "POST":
        science = float(request.form["science"])
        maths = float(request.form["maths"])
        c = float(request.form["c"])
        ds = float(request.form["ds"])
        total_score = (science + maths + c + ds)/4

        return redirect(url_for("success",score = total_score ))
    return render_template("index.html")

app.run(debug=True)