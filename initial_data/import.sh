#!/bin/sh
# Import areas (countries and continents)
mongoimport --db webindex --collection areas < areas.json

# Import indicators
mongoimport --db webindex --collection indicators < indicators.json

# Import observations
mongoimport --db webindex --collection observations < observations.json