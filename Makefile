install: ## Install server with its dependencies
	docker-compose build

start: ## Start dev server in its docker container
	docker-compose up dev-server

test: ## Run tests in a docker container
	docker-compose up test
