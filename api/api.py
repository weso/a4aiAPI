# #########################################################################################
##                                  INITIALISATIONS                                     ##
##########################################################################################
# Flask
from flask import Flask, request, render_template, Response
import json
from functools import wraps


import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../../a4aiDom'))
from infrastructure.mongo_repos.area_repository import AreaRepository
from infrastructure.mongo_repos.indicator_repository import IndicatorRepository
from infrastructure.mongo_repos.observation_repository import ObservationRepository
from infrastructure.errors.errors import RepositoryError
from flask.ext.cache import Cache

# bson
from bson.json_util import dumps


cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
cache.init_app(app)

TIMEOUT = 30  # timeout to clean cache in seconds

##########################################################################################
##                                 JSONP DECORATOR                                      ##
##########################################################################################

def json_response(data, request, status=200):
    json = dumps(data, ensure_ascii=False).encode('utf-8')
    callback = request.args.get('callback', False)
    if callback:
        return Response(str(callback) + '(' + str(json) + ');', mimetype="application/javascript; charset=utf-8")
    return Response(json, mimetype="application/json; charset=utf-8", status=status)


def json_response_ok(request, data):
    data = success(data)
    return json_response(data, request)


def json_response_error(request, data):
    data = error(data)
    return json_response(data, request, status=400)


def json_encoder(request, data):
    # Check first in order to convert to dict
    if isinstance(data, list):
        data = [data_element.to_dict() for data_element in data]
    else:
        data = data.to_dict()

    return json_response_ok(request, data)


##########################################################################################
##                                SUCCESS FUNCTION                                      ##
##########################################################################################

def success(data):
    return {"success": True, "data": data}


##########################################################################################
##                                  ERROR FUNCTION                                      ##
##########################################################################################

def error(data):
    return {"success": False, "error": data}

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
@cache.memoize(timeout=TIMEOUT)
def list_areas():
    """List all areas (countries and continents)"""
    order = request.args.get('orderBy')

    areas = AreaRepository(url_root=request.url_root).find_areas(order)

    return json_encoder(request, areas)


@app.route("/areas/countries")
@cache.memoize(timeout=TIMEOUT)
def list_countries():
    order = request.args.get('orderBy')
    countries = AreaRepository(url_root=request.url_root).find_countries(order)
    return json_encoder(request, countries)


@app.route("/areas/continents")
@cache.memoize(timeout=TIMEOUT)
def list_continents():
    order = request.args.get('orderBy')
    continents = AreaRepository(url_root=request.url_root).find_continents(order)
    return json_encoder(request, continents)


@app.route("/areas/<area_code>")
@cache.memoize(timeout=TIMEOUT)
def show_area(area_code):
    area = AreaRepository(url_root=request.url_root).find_countries_by_code_or_income(area_code)
    return json_encoder(request, area)


@app.route("/areas/<area_code>/countries")
@cache.memoize(timeout=TIMEOUT)
def show_area_countries(area_code):
    order = request.args.get('orderBy')
    countries = AreaRepository(url_root=request.url_root).find_countries_by_continent_or_income_or_type(area_code, order)
    return json_encoder(request, countries)


##########################################################################################
##                                     INDICATORS                                       ##
##########################################################################################

@app.route("/indicators")
@cache.memoize(timeout=TIMEOUT)
def list_indicators():
    indicators = IndicatorRepository(url_root=request.url_root).find_indicators()

    return json_encoder(request, indicators)


@app.route("/indicators/index")
@cache.memoize(timeout=TIMEOUT)
def show_index():
    _index = IndicatorRepository(url_root=request.url_root).find_indicators_index()
    return json_encoder(request, _index)


@app.route("/indicators/subindices")
@cache.memoize(timeout=TIMEOUT)
def list_subindices():
    subindices = IndicatorRepository(url_root=request.url_root).find_indicators_sub_indexes()
    return json_encoder(request, subindices)


@app.route("/indicators/primary")
@cache.memoize(timeout=TIMEOUT)
def list_primary():
    primary = IndicatorRepository(url_root=request.url_root).find_indicators_primary()
    return json_encoder(request, primary)


@app.route("/indicators/secondary")
@cache.memoize(timeout=TIMEOUT)
def list_secondary():
    secondary = IndicatorRepository(url_root=request.url_root).find_indicators_secondary()
    return json_encoder(request, secondary)


@app.route("/indicators/<indicator_code>")
@cache.memoize(timeout=TIMEOUT)
def show_indicator(indicator_code):
    indicator = IndicatorRepository(url_root=request.url_root).find_indicator_by_code(indicator_code)
    return json_encoder(request, indicator)


@app.route("/indicators/<indicator_code>/indicators")
@cache.memoize(timeout=TIMEOUT)
def list_indicator_indicators(indicator_code):
    indicator = IndicatorRepository(url_root=request.url_root).find_indicator_by_code(indicator_code)

    if indicator is None:
        return json_encoder(request, indicator)

    indicators = IndicatorRepository(url_root=request.url_root).find_indicators_indicators(indicator)
    return json_encoder(request, indicators)


@app.route("/indicators/<indicator_code>/primary")
@cache.memoize(timeout=TIMEOUT)
def list_indicator_primary(indicator_code):
    indicator = IndicatorRepository(url_root=request.url_root).find_indicator_by_code(indicator_code)

    if indicator is None:
        return json_encoder(request, indicator)

    primary = IndicatorRepository(url_root=request.url_root).find_indicators_primary(indicator)
    return json_encoder(request, primary)


@app.route("/indicators/<indicator_code>/secondary")
@cache.memoize(timeout=TIMEOUT)
def list_indicator_secondary(indicator_code):
    indicator = IndicatorRepository(url_root=request.url_root).find_indicator_by_code(indicator_code)

    if indicator is None:
        return json_encoder(request, indicator)

    secondary = IndicatorRepository(url_root=request.url_root).find_indicators_secondary(indicator)
    return json_encoder(request, secondary)


##########################################################################################
##                                    OBSERVATIONS                                      ##
##########################################################################################
@app.route("/observations")
@cache.memoize(timeout=TIMEOUT)
def list_observations():
    observations = ObservationRepository(url_root=request.url_root).find_observations()
    return json_encoder(request, observations)


@app.route("/observations/<indicator_code>")
@cache.memoize(timeout=TIMEOUT)
def list_observations_by_indicator(indicator_code):
    observations = ObservationRepository(url_root=request.url_root).find_observations(indicator_code)
    return json_encoder(request, observations)


@app.route("/observations/<indicator_code>/<area_code>")
@cache.memoize(timeout=TIMEOUT)
def list_observations_by_indicator_and_country(indicator_code, area_code):
    observations = ObservationRepository(url_root=request.url_root).find_observations(indicator_code, area_code)
    return json_encoder(request, observations)


@app.route("/observations/<indicator_code>/<area_code>/<year>")
@cache.memoize(timeout=TIMEOUT)
def list_observations_by_indicator_and_country_and_year(indicator_code, area_code, year):
    observations = ObservationRepository(url_root=request.url_root).find_observations(indicator_code, area_code, year)
    return json_encoder(request, observations)


##########################################################################################
##                                      STATISTICS                                      ##
##########################################################################################
@app.route("/statistics")
@cache.memoize(timeout=TIMEOUT)
def list_observations_statistics():
    statistics = ObservationRepository(url_root=request.url_root).find_observations_statistics()
    return json_encoder(request, statistics)


@app.route("/statistics/<indicator_code>")
@cache.memoize(timeout=TIMEOUT)
def list_observations_by_indicator_statistics(indicator_code):
    statistics = ObservationRepository(url_root=request.url_root).find_observations_statistics(indicator_code)
    return json_encoder(request, statistics)


@app.route("/statistics/<indicator_code>/<area_code>")
@cache.memoize(timeout=TIMEOUT)
def list_observations_by_indicator_and_country_statistics(indicator_code, area_code):
    statistics = ObservationRepository(url_root=request.url_root).find_observations_statistics(indicator_code, area_code)
    return json_encoder(request, statistics)


@app.route("/statistics/<indicator_code>/<area_code>/<year>")
@cache.memoize(timeout=TIMEOUT)
def list_observations_by_indicator_and_country_and_year_statistics(indicator_code, area_code, year):
    statistics = ObservationRepository(url_root=request.url_root).find_observations_statistics(indicator_code, area_code, year)
    return json_encoder(request, statistics)

##########################################################################################
##                                   VISUALISATION                                      ##
##########################################################################################
@app.route("/visualisations")
@cache.memoize(timeout=TIMEOUT)
def list_observations_visualisations():
    visualisation = ObservationRepository(url_root=request.url_root).find_observations_visualisation()
    return json_encoder(request, visualisation)


@app.route("/visualisations/<indicator_code>")
@cache.memoize(timeout=TIMEOUT)
def list_observations_by_indicator_visualisations(indicator_code):
    visualisation = ObservationRepository(url_root=request.url_root).find_observations_visualisation(indicator_code)
    return json_encoder(request, visualisation)


@app.route("/visualisations/<indicator_code>/<area_code>")
@cache.memoize(timeout=TIMEOUT)
def list_observations_by_indicator_and_country_visualisations(indicator_code, area_code):
    visualisation = ObservationRepository(url_root=request.url_root)\
        .find_observations_visualisation(indicator_code, area_code)
    return json_encoder(request, visualisation)


@app.route("/visualisations/<indicator_code>/<area_code>/<year>")
@cache.memoize(timeout=TIMEOUT)
def list_observations_by_indicator_and_country_and_year_visualisations(indicator_code, area_code, year):
    visualisation = ObservationRepository(url_root=request.url_root)\
        .find_observations_visualisation(indicator_code, area_code, year)
    return json_encoder(request, visualisation)


##########################################################################################
##                             VISUALISATION GROUPED BY AREA                            ##
##########################################################################################
@app.route("/visualisationsGroupedByArea")
@cache.memoize(timeout=TIMEOUT)
def list_observations_visualisations_grouped_by_area():
    visualisation = ObservationRepository(url_root=request.url_root)\
        .find_observations_grouped_by_area_visualisation()
    return json_encoder(request, visualisation)


@app.route("/visualisationsGroupedByArea/<indicator_code>")
@cache.memoize(timeout=TIMEOUT)
def list_observations_by_indicator_visualisations_grouped_by_area(indicator_code):
    visualisation = ObservationRepository(url_root=request.url_root)\
        .find_observations_grouped_by_area_visualisation(indicator_code)
    return json_encoder(request, visualisation)


@app.route("/visualisationsGroupedByArea/<indicator_code>/<area_code>")
@cache.memoize(timeout=TIMEOUT)
def list_observations_by_indicator_and_country_visualisations_grouped_by_area(indicator_code, area_code):
    visualisation = ObservationRepository(url_root=request.url_root)\
        .find_observations_grouped_by_area_visualisation(indicator_code, area_code)
    return json_encoder(request, visualisation)


@app.route("/visualisationsGroupedByArea/<indicator_code>/<area_code>/<year>")
@cache.memoize(timeout=TIMEOUT)
def list_observations_by_indicator_and_country_and_year_visualisations_grouped_by_area(indicator_code, area_code, year):
    visualisation = ObservationRepository(url_root=request.url_root)\
        .find_observations_grouped_by_area_visualisation(indicator_code, area_code, year)
    return json_encoder(request, visualisation)

##########################################################################################
##                                        YEARS                                         ##
##########################################################################################

@app.route("/years")
@cache.memoize(timeout=TIMEOUT)
def list_observations_years():
    years = ObservationRepository(url_root=request.url_root).get_year_list()
    return json_encoder(request, years)


@app.route("/years/array")
@cache.memoize(timeout=TIMEOUT)
def list_observations_years_array():
    years = ObservationRepository(url_root=request.url_root).get_year_list()
    years_array = [year.value for year in years]
    return json_response_ok(request, years_array)


@app.errorhandler(RepositoryError)
def handle_repository_error(error):
    return json_response_error(request, error.message)


##########################################################################################
##                                        MAIN                                          ##
##########################################################################################

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
