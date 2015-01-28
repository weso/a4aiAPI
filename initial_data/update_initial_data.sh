#!/bin/bash


db="webindex"
mongo $db --eval "db.areas.remove({})"
mongo $db --eval "db.indicators.remove({})"
mongo $db --eval "db.observations.remove({})"

cd a4aiAPI/initial_data
mongoimport --db $db --collection areas < areas.json
mongoimport --db $db --collection indicators < indicators.json
mongoimport --db $db --collection observations < observations.json
cd ../..
