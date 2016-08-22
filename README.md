# bowtie-demo

This is hosted on a free dyno on Heroku, so if it doesn't load immediately the dyno probably needs a minute to wake up.

https://bowtie-demo.herokuapp.com/

To run locally, first install the requirements.

```
conda install --file conda-requirements.txt
pip install -r requirements.txt
```

You also need Install [node](https://nodejs.org/en/) and install `webpack` globally.

```
npm install -g webpack
```

Then run the python script.

```
./example.py
```

Then assuming everything builds correctly, run

```
./build/src/server.py
```

Then go to <http://localhost:9991> on your local machine.
