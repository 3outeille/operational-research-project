# operational-research-project

# Setup (Linux)

## First time only
```
virtualenv ero-env
source ero-env/bin/activate
pip install -r requirements.txt
```

- To link environnemnt with Jupyter Notebook (make sure your env is activated)

```
python -m ipykernel install --user --name=ero-env
jupyter notebook
# -> In jupyter notebook, click on Noyau > Changer de noyau > nom_de_ton_env
```

## Other times

- Just need to activate your environnement
```
source ero-env/bin/activate
```

# Architecture

* `src/`
  * `theory/` : a sub-tree dedicated to the study of the theoretical case 
  * `application/` : a sub-tree dedicated to the study of the real case of the city of Montreal 
* `AUTHORS`
* `README.md`
* `synthesis.pdf` : summary of the team's reflections 
* `LINKS` : link to the video presentation of the solution
* `script.py` : a script running a demo of the solution 
