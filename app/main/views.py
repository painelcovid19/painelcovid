from flask import render_template, redirect, url_for, session, flash
from app.main.forms import Login, Sigup
from . import main
from app.main.repositor.user import UserRepositor
import json
import plotly
import plotly.graph_objs as go


user_repo = UserRepositor(table_name="users")

# importando graficos de casos confirmados e obitos
from .graficos.main import (
    confirmated_cases_acarape,
    confirmated_cases_redencao,
    confirmated_cases_SFC,
    death_cases_acarape,
    death_cases_redencao,
    death_cases_SFC
)

# importando dados totais de casos confirmados e obitos(actualiza os cards)
from .graficos.packages.utils import (
    last_actualization_date_acarape,
    last_actualization_date_redencao,
    last_actualization_date_SFC,

  acarape_total_confirmated_data,
  acarape_total_death_data,
  redencao_total_confirmated_data,
  redencao_total_death_data,
  SFC_total_confirmated_data,
  SFC_tota_death_data
)

from .graficos.main import mapas
from .graficos.vacinas_html import vacinas, data, layout
from .graficos.rt_html import graf

# import plotly.io as pio
cf_acarape = json.dumps(confirmated_cases_acarape, cls=plotly.utils.PlotlyJSONEncoder)
death_acarape = json.dumps(death_cases_acarape, cls=plotly.utils.PlotlyJSONEncoder)
confirmated_redencao = json.dumps(confirmated_cases_redencao, cls=plotly.utils.PlotlyJSONEncoder)
death_redencao = json.dumps(death_cases_redencao, cls=plotly.utils.PlotlyJSONEncoder)
confirmated_SFC = json.dumps(confirmated_cases_SFC, cls=plotly.utils.PlotlyJSONEncoder)
death_SFC = json.dumps(death_cases_SFC, cls=plotly.utils.PlotlyJSONEncoder)

# mapas
mapas_plot = json.dumps(graf[0], cls=plotly.utils.PlotlyJSONEncoder)
mapas_plot1 = json.dumps(graf[1], cls=plotly.utils.PlotlyJSONEncoder)
mapas_plot2 = json.dumps(graf[2], cls=plotly.utils.PlotlyJSONEncoder)
mapas_plot3 = json.dumps(graf[3], cls=plotly.utils.PlotlyJSONEncoder)
mapas_plot4 = json.dumps(graf[4], cls=plotly.utils.PlotlyJSONEncoder)

# estimativas rt
rt_plot = json.dumps(mapas[0], cls=plotly.utils.PlotlyJSONEncoder)
rt_plot1 = json.dumps(mapas[0], cls=plotly.utils.PlotlyJSONEncoder)
rt_plot2= json.dumps(mapas[1], cls=plotly.utils.PlotlyJSONEncoder)
rt_plot3 = json.dumps(mapas[2], cls=plotly.utils.PlotlyJSONEncoder)
rt_plot4 = json.dumps(mapas[3], cls=plotly.utils.PlotlyJSONEncoder)

# vacinas
vacinas_etaria = go.Figure(data=data, layout=layout)
vacina_plot1 = json.dumps(vacinas, cls=plotly.utils.PlotlyJSONEncoder)
vacinas_plot2 = json.dumps(vacinas_etaria, cls=plotly.utils.PlotlyJSONEncoder)

@main.route("/", methods=["GET"])
def index():
    name = None
    if session.get("name"):
        name = session["name"]
    return render_template("inicio_b.html",
                  total_case_redencao = redencao_total_confirmated_data,
                  total_death_redencao = redencao_total_death_data,
                  last_actualization_redencao = last_actualization_date_redencao,
                  total_case_acarape = acarape_total_confirmated_data,
                  total_death_acarape = acarape_total_death_data,
                  last_actualization_acarape = last_actualization_date_acarape,
                  total_case_SFC = SFC_total_confirmated_data,
                  total_death_SFC = SFC_tota_death_data,
                  last_actualization_SFC = last_actualization_date_SFC,
                  cf_acarape = cf_acarape,
                  death_acarape = death_acarape, 
                  confirmated_redencao = confirmated_redencao,
                  death_redencao = death_redencao,
                  confirmated_SFC = confirmated_SFC,
                  death_SFC = death_SFC,
                  name=name
                          ), 200
   
@main.route("/mapas", methods=["GET"])
def mapas():
    name = session["name"]
    return render_template("mapas_b.html", 
                  Plot = mapas_plot,
                  Plot1 = mapas_plot1,
                  Plot2 = mapas_plot2,
                  Plot3 = mapas_plot3,
                  title = "mapas de macrorregiões",
                  name=name
                          ), 200
 
@main.route("/estimativas_rt", methods=["GET"])
def estimativas_rt():
    name = session["name"]
    return render_template("estimativas_b.html", 
                    Plot = rt_plot,
                    Plot1 = rt_plot1,
                    Plot2 = rt_plot2,
                    Plot3 = rt_plot3,
                    Plot4 = rt_plot4,
                    title="estimativas R(t)",
                    name=name
                            ), 200
 

@main.route("/vacinas", methods=["GET"])
def vacinas():
    name= session["name"]
    return render_template("vacina_b.html", 
                    Plot1 = vacina_plot1,
                    Plot2 = vacinas_plot2,
                    title = "vacinas",
                    name=name
                            ), 200
 
 
@main.route("/sobre", methods=["GET"])
def sobre():
    name = session["name"]
    return render_template("sobre_b.html", title="sobre", name=name), 200

# User authentication

@main.route("/login", methods=["GET", "POST"])
def login():
        login_form = Login()
        return render_template("login.html", form=login_form), 200

@main.route("/signup", methods=["GET", "POST"])
def signup():
        signup_form = Sigup()
        if signup_form.validate_on_submit():
                print("validou")
                name = signup_form.name.data
                email = signup_form.email.data
                password = signup_form.password.data
                response = user_repo.insert(name, email, password)
                if response:
                    flash("usuário cadastrado")
                return redirect(url_for("main.signup"))
        return render_template("signup.html", form=signup_form), 200