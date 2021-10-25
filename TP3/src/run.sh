coverage run -m --source=. --omit=exemple.py,main.py,test_*.py,renege.py,text_cleaner.py --branch unittest test_crud.py test_email_analyzer.py test_vocabulary_creator.py
coverage report