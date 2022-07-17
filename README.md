**LoopCoin** 

Loopcoin is a minimal bitcoin-like PoW blockchain.


**Install all packages**

```
pip install -r requirements.txt
```

**Run the tests**

Make sure to activate the virtual environment.

```
python -m pytest core/tests
```

**Run a peer instance**

Make sure to activate venv.

```
set PEER=True
python -m core.app
```

**Run the client**

```
npm start in ./client directory.
```

**Seed the backend with data**

Make sure to activate the virtual environment.

```
set SEED_DATA=True && python -m core.app
```
