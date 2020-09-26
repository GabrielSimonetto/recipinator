install:
	poetry install

crawler:
	cd recipinator/scrapers
	poetry run scrapy crawl recipes -o data.json
	cd ../..

database:
	poetry run python recipinator/database/db.py

init_project: install crawler database