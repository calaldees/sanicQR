DOCKER_IMAGE:=qr
DOCKER_RUN:=docker run --rm -it --publish 8000:8000 --volume ${PWD}:/app/ ${DOCKER_IMAGE}

build:
	docker build --tag ${DOCKER_IMAGE} .
run: build
	${DOCKER_RUN}
shell:
	${DOCKER_RUN} /bin/sh
test: build
	${DOCKER_RUN} python3 -m doctest --fail-fast app.py
