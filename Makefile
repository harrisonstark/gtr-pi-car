# Build the Docker container
build:
	docker build -t gtr-pi-car .

# Run the Docker container and enter a bash shell
run:
	docker run -it --rm -p 7171:7171 --env-file .env gtr-pi-car

# Shortcut to build, run, install, and start the app in development mode
start: build run