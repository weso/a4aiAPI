# #########################################################################################
##                                  INITIALISATIONS                                     ##
##########################################################################################
# Flask
from flask import Flask, request, render_template, Response
import json
from functools import wraps

app = Flask(__name__)
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../../wixDom'))
from infrastructure.mongo_repos.area_repository import AreaRepository
from infrastructure.mongo_repos.indicator_repository import IndicatorRepository
from infrastructure.mongo_repos.observation_repository import ObservationRepository
from infrastructure.mongo_repos.ranking_repository import RankingRepository

# bson
from bson.json_util import dumps

##########################################################################################
##                                 JSONP DECORATOR                                      ##
##########################################################################################

def JSONEncoder(request, data):
    json = dumps(data)

    callback = request.args.get('callback', False)

    if callback:
        return Response(str(callback) + '(' + str(json) + ');', mimetype = "application/javascript")

    return Response(json, mimetype = "application/json")


##########################################################################################
##                                        ROOT                                          ##
##########################################################################################

@app.route("/")
def index():
    """API Documentation"""
    return render_template('help.html')


##########################################################################################
##                                       AREAS                                          ##
##########################################################################################

@app.route("/areas")
def list_areas():
    """List all areas (countries and continents)"""
    order = request.args.get('orderBy')

    areas = AreaRepository(url_root=request.url_root).find_areas(order)

    return JSONEncoder(request, areas)


@app.route("/areas/countries")
def list_countries():
    order = request.args.get('orderBy')
    countries = AreaRepository(url_root=request.url_root).find_countries(order)
    return JSONEncoder(request, countries)


@app.route("/areas/continents")
def list_continents():
    order = request.args.get('orderBy')
    continents = AreaRepository(url_root=request.url_root).find_continents(order)
    return JSONEncoder(request, continents)


@app.route("/areas/<area_code>")
def show_area(area_code):
    area = AreaRepository(url_root=request.url_root).find_countries_by_code_or_income(area_code)
    return JSONEncoder(request, area)


@app.route("/areas/<area_code>/countries")
def show_area_countries(area_code):
    order = request.args.get('orderBy')
    countries = AreaRepository(url_root=request.url_root).find_countries_by_continent_or_income(area_code, order)
    return JSONEncoder(request, countries)


##########################################################################################
##                                     INDICATORS                                       ##
##########################################################################################

@app.route("/indicators")
def list_indicators():
    indicators = IndicatorRepository(url_root=request.url_root).find_indicators()

    return JSONEncoder(request, indicators)


@app.route("/indicators/index")
def show_index():
    _index = IndicatorRepository(url_root=request.url_root).find_indicators_index()
    return JSONEncoder(request, _index)


@app.route("/indicators/subindices")
def list_subindices():
    subindices = IndicatorRepository(url_root=request.url_root).find_indicators_sub_indexes()
    return JSONEncoder(request, subindices)


@app.route("/indicators/components")
def list_components():
    components = IndicatorRepository(url_root=request.url_root).find_indicators_components()
    return JSONEncoder(request, components)


@app.route("/indicators/primary")
def list_primary():
    primary = IndicatorRepository(url_root=request.url_root).find_indicators_primary()
    return JSONEncoder(request, primary)


@app.route("/indicators/secondary")
def list_secondary():
    secondary = IndicatorRepository(url_root=request.url_root).find_indicators_secondary()
    return JSONEncoder(request, secondary)


@app.route("/indicators/<indicator_code>")
def show_indicator(indicator_code):
    indicator = IndicatorRepository(url_root=request.url_root).find_indicators_by_code(indicator_code)
    return JSONEncoder(request, indicator)


@app.route("/indicators/<indicator_code>/components")
def list_indicator_components(indicator_code):
    indicator = IndicatorRepository(url_root=request.url_root).find_indicators_by_code(indicator_code)

    if indicator["success"] is False:
        return JSONEncoder(request, indicator)

    components = IndicatorRepository(url_root=request.url_root).find_indicators_components(indicator["data"])
    return JSONEncoder(request, components)


@app.route("/indicators/<indicator_code>/indicators")
def list_indicator_indicators(indicator_code):
    indicator = IndicatorRepository(url_root=request.url_root).find_indicators_by_code(indicator_code)

    if indicator["success"] is False:
        return JSONEncoder(request, indicator)

    indicators = IndicatorRepository(url_root=request.url_root).find_indicators_indicators(indicator["data"])
    return JSONEncoder(request, indicators)


@app.route("/indicators/<indicator_code>/primary")
def list_indicator_primary(indicator_code):
    indicator = IndicatorRepository(url_root=request.url_root).find_indicators_by_code(indicator_code)

    if indicator["success"] is False:
        return JSONEncoder(request, indicator)

    primary = IndicatorRepository(url_root=request.url_root).find_indicators_primary(indicator["data"])
    return JSONEncoder(request, primary)


@app.route("/indicators/<indicator_code>/secondary")
def list_indicator_secondary(indicator_code):
    indicator = IndicatorRepository(url_root=request.url_root).find_indicators_by_code(indicator_code)

    if indicator["success"] is False:
        return JSONEncoder(request, indicator)

    secondary = IndicatorRepository(url_root=request.url_root).find_indicators_secondary(indicator["data"])
    return JSONEncoder(request, secondary)


##########################################################################################
##                                    OBSERVATIONS                                      ##
##########################################################################################
@app.route("/observations")
def list_observations():
    observations = ObservationRepository(url_root=request.url_root).find_observations()
    return JSONEncoder(request, observations)

@app.route("/linked-observations")
def list_linked_observations():
    linked_obs = ObservationRepository(url_root=request.url_root).find_linked_observations()
    return JSONEncoder(request, linked_obs)

@app.route("/observations/<indicator_code>")
def list_observations_by_indicator(indicator_code):
    observations = ObservationRepository(url_root=request.url_root).find_observations(indicator_code)
    return JSONEncoder(request, observations)

@app.route("/observations/<indicator_code>/<area_code>")
def list_observations_by_indicator_and_country(indicator_code, area_code):
    observations = ObservationRepository(url_root=request.url_root).find_observations(indicator_code, area_code)
    return JSONEncoder(request, observations)


@app.route("/observations/<indicator_code>/<area_code>/<year>")
def list_observations_by_indicator_and_country_and_year(indicator_code, area_code, year):
    observations = ObservationRepository(url_root=request.url_root).find_observations(indicator_code, area_code, year)
    return JSONEncoder(request, observations)


##########################################################################################
##                                        YEARS                                         ##
##########################################################################################

@app.route("/years")
def list_observations_years():
    years = ObservationRepository(url_root=request.url_root).get_year_list()
    return JSONEncoder(request, years)

@app.route("/years/array")
def list_observations_years_array():
    years = ObservationRepository(url_root=request.url_root).get_year_array()
    return JSONEncoder(request, years)

##########################################################################################
##                                    VISUALISATIONS                                    ##
##########################################################################################

@app.route("/visualisations/<indicator_code>/<area_code>/<year>")
def list_visualisations(indicator_code, area_code, year):
    visualisations = ObservationRepository(url_root=request.url_root).find_visualisations(indicator_code, area_code, year)
    return JSONEncoder(request, visualisations)

##########################################################################################
##                                       RANKINGS                                       ##
##########################################################################################

@app.route("/rankings")
def list_last_rankings():
    years = ObservationRepository(url_root=request.url_root).get_year_list()
    year = years["data"][0]["value"]
    rankings = RankingRepository(url_root=request.url_root).find_rankings(year)
    return JSONEncoder(request, rankings)

@app.route("/rankings/<year>")
def list_rankings(year):
    rankings = RankingRepository(url_root=request.url_root).find_rankings(year)
    return JSONEncoder(request, rankings)

##########################################################################################
##                                         HOME                                        ##
##########################################################################################

@app.route("/home/<indicators>/<limits>/<tendencies>/<values>")
def list_home(indicators, limits, tendencies, values):
    years = ObservationRepository(url_root=request.url_root).get_year_array()

    indicators = indicators.upper().strip().split(",")
    limits = limits.upper().strip().split(",")
    tendencies = tendencies.upper().strip().split(",")
    values = values.upper().strip().split(",")

    if years["success"] is True:
        year = years["data"][0]
        rankings = RankingRepository(url_root=request.url_root).find_rankings(year)
        result = {
            "rankings": rankings
        }

        for i in range(len(indicators)):
            indicator = indicators[i]
            limit = limits[i] if i < len(limits) else ""
            tendency = tendencies[i] if i < len(tendencies) else -1
            value = values[i] if i < len(values) else ""

            index = str(i + 1)

            observations = ObservationRepository(url_root=request.url_root).find_observations(indicator, "ALL", year)
            observations = observations["data"] if observations["data"] else []

            percentage = get_percentage(observations, limit, tendency) if limit else value

            result["observations%s" % index] = observations
            result["percentage%s" % index] = percentage

    return JSONEncoder(request, result)

def get_percentage(observations, limit, tendency):
    count = 0
    sum = 0
    tendency = num(tendency)
    limit = num(limit)

    for observation in observations:
        value = observation["value"]

        if tendency > 0 and value >= limit:
            sum = sum + 1

        if tendency < 0 and value <= limit:
            sum = sum + 1

        count = count + 1

    percentage = sum * 100.0 / count if count > 0 else 0

    return round(percentage)

def num(s):
    try:
        return int(s)
    except ValueError:
        return 0

##########################################################################################
##                                        MAIN                                          ##
##########################################################################################

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
