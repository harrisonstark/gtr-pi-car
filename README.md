# gtr-pi-car
Gator Raspberry Pi Car Server
 
## Starting the app
As the app currently stands, from the root directory, run `python -m uvicorn src.app:app --host 0.0.0.0 --port 7171`
 
For the first time running, install Poetry and dependencies:
```bash
pip install poetry --break-system-packages
python -m poetry install
```
 
## Accessing the app
Make requests to the various routes on localhost:7171, or access it from gtr-pi-driver
 
