install:
	python -m pip install -r requirements.txt

data:
	python run_pipeline.py

notebook:
	jupyter notebook notebooks/analise_luz_para_todos.ipynb

dashboard:
	streamlit run dashboard/streamlit/app.py
