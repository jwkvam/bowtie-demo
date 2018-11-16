# bowtie-demo

This is hosted on a free dyno on Heroku, so if it doesn't load immediately the dyno probably needs a minute to wake up.

https://bowtie-demo.herokuapp.com/

To run locally, first install the requirements:

```
conda install --file conda-requirements.txt
pip install -r requirements.txt
```

You also need to install [yarn](https://nodejs.org/en/) and yarn:

```
conda install yarn -c conda-forge
```

Then build the app:

```
./example.py build
```

Then assuming everything builds correctly, serve it:

```
./example.py serve
```

Then go to <http://localhost:9991> on your local machine.
