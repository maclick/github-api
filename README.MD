
# Github api

My email in recruitment process: ```macius.bielik@gmail.com```

W swoim rozwiązaniu korzystam z bibliotek pythona:
 - requests
 - json
 - fastapi

Github api ogranicza ilość wysłanych requestów w ciągu godziny 
przez co rozwiązanie może nie działać, jeśli będziemy sprawdzać 
użytkowników z większą ilością repozytoriów, 
rozwiązaniem tego problemu może być podanie w pliku auth.json danych
konta na Github, czyli uzupełnienie pola username nazwą użytkownika
oraz pola token wartością access token z Githuba

Sposób użycia:
 - uruchomić aplikację przy użyciu
      ```
      uvicorn api:app
      ```
 - w 4 linii pojawia się adres, pod którym działa aplikacj, np:
 ```
  INFO:     Uvicorn running on http://127.0.0.1:8000)
```
 - aby sprawdzić użytkownika należy przejść pod zwrócony adres
   i podstrony:
```
127.0.0.1:8000/check_user?username=allegro
```
-  (wartość allegro zamieniamy na username dowolnego użytkownika, którego chcemy sprawdzić)

