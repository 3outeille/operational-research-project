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
