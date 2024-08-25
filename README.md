# gtr-pi-car
Gator Raspberry Pi Car Server

## Starting the app
As the app currently stands, from the root directory, run 'python -m uvicorn src.app:app --host 0.0.0.0 --port 7171'
Ensure you have a .env file in the root directory with both MONGODB_URI and PORT (optional) set
For the first time running, please run 'pip install -r requirements.txt' from the root directory

I have an untested Dockerfile and Makefile to run all in one command, not ready yet though

## Accessing the app
Make requests to the various routes on localhost:7171, or access it from gtr-pi-driver