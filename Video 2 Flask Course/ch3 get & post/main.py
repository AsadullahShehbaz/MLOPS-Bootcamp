from flask import Flask, render_template,request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/myform", methods=["GET", "POST"])
def formSubmit():
    if request.method == "POST":
       name =  request.form["name"]
       return f"Welcome, {name}"
    
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)