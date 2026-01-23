run:
	echo "Get depot from TR"
	cd data && uvx pytr@latest export_transactions
	rm data/all_events.json

	echo "Calculate stock amounts"
	python amounts.py

	echo "Get stock prices"
	python price.py

	echo "Move csv to docker volume"
	./transfer_data

update:
	echo "Update prices"
	python price.py

	echo "upload :)"
	./transfer_data
