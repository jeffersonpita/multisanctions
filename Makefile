all: | unit-test run;

setup:
	docker-compose build

run: setup
	docker-compose up

unit-test: ;

#smoke-test: setup
#	docker-compose run --rm test
