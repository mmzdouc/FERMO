from flask import Blueprint, render_template

views= Blueprint(__name__, "views")

@views.route("/")
def landing():
    return render_template('landing.html')

@views.route("/loading")
def loading():
    return render_template('loading.html')


@views.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')


@views.route("/processing")
def processing():
    return render_template('processing.html')

