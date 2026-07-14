1. Needed libraries are saved into requirements.txt
2. Everything is being run in .venv
   
To activate it, use: 
```
.\.venv\Scripts\activate to activate
```
   
To deactivate it, use:
```
deactivate
```

3. Run app with 
```
fastapi dev
```

4. Tests are run by 
```
python -m pytest
```


Troubleshoot:
If you have issues installing sqlalchemy because of greenlet, simply install greenlet first with 
```
pip install greenlet==2.0.2 --only-binary :all:
```