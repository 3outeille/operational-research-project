#!/bin/bash

if [[ "$VIRTUAL_ENV" != "$PWD/ero-env" ]]; then
  echo "Installing virtualenv..."
  virtualenv ero-env
  echo "Source virtualenv..."
  source ero-env/bin/activate
  echo "Install depedencies..."
  pip install -r requirements.txt
  python setup.py clean
fi

echo 
echo "Run demonstrations.."
echo "Drone demo..."
echo "map - Montréal Centre-Ville"
python src/application/solver.py --mode=drone --map=downtown_montreal_graph

echo 
echo "map - Montréal (can take up to 10 mins if your network connection is slow)"
python src/application/solver.py --mode=drone --map=montreal_graph

echo 
echo "Run tests..."
cd src/theory
python test.py
cd -

echo
echo "Déneigeuse demo..."
echo "map - Montréal"
echo "algo - First match"
echo "nb déneigeuse - 4"
python src/application/solver.py --mode=deneigeuse --map=montreal_di_graph --algo=first_match --nb_deneigeuse=4

echo
echo "map - Montréal"
echo "algo - Best match"
echo "nb déneigeuse - 10"
python src/application/solver.py --mode=deneigeuse --map=montreal_di_graph --algo=best_match --nb_deneigeuse=10