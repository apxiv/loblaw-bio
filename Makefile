.PHONY: setup pipeline dashboard

setup:
	python3 -m pip install -r requirements.txt

pipeline:
	python3 load_data.py
	python3 analyze.py
	python3 compare_response.py
	python3 subset.py

dashboard:
	python3 -m streamlit run dashboard.py --server.address 0.0.0.0 --server.port 8501
