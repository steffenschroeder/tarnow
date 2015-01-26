from flask import Flask, redirect
from flask import render_template
from flask_bootstrap import Bootstrap

from switch import *
import config


app = Flask(__name__)
Bootstrap(app)
app.config.from_object(config)


@app.route('/')
def show_switches():
    switches = get_switches()
    return render_template('switch.html', switches=switches)


def get_switches():
    switches = []
    switches_from_config = config.switches
    for switch in switches_from_config.keys():
        s = Switch(switch)
        b = " disabled" if (s.is_skip_next() or s.is_skip_all()) else ""
        switches.append(dict(name=s.name,
                             is_skip=s.is_skip_next(),
                             is_permanent_skip=s.is_skip_all(),
                             enabled_class=b))
    return switches


def homepage():
    return redirect("/", code=302)


@app.route('/on/<string:switch>')
def on(switch):
    toggle_switch(switch, 1)
    return homepage()


@app.route('/off/<string:switch>')
def off(switch):
    toggle_switch(switch, 0)
    return homepage()


def toggle_switch(switch, status):
    s = Switch(switch)
    s.toggle(status)


@app.route('/createtemporary/<string:switch>')
def create_p_skip(switch):
    s = Switch(switch)
    s.skip_next()
    return homepage()


@app.route('/createpermanent/<string:switch>')
def create_t_skip(switch):
    s = Switch(switch)
    s.skip_all()
    return homepage()


@app.route('/deletepermanent/<string:switch>')
def delete_p_skip(switch):
    s = Switch(switch)
    s.dont_skip_all()
    return homepage()


@app.route('/deletetemporary/<string:switch>')
def delete_t_skip(switch):
    s = Switch(switch)
    s.dont_skip_next()
    return homepage()


if __name__ == '__main__':
    enable_debug = False
    app.run(host='0.0.0.0', port=8080, debug=enable_debug)
