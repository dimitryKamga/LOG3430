python -m coverage run -m --source=. --omit=main.py,renege.py,text_cleaner.py,test_*.py,venv/* --branch unittest test_crud.py test_email_analyzer.py test_vocabulary_creator.py
python -m coverage report | tee coverage_report.txt
coverage html