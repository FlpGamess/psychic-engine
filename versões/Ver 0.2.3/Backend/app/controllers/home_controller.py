from flask import render_template

#Lógica para a chamada da página principal
def home():
    return render_template("homepage.html")