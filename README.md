# speed-limit-signs-detection

Program wykorzystuje bibliotekę openCV do wykrywania znaków ograniczeń prędkości na filmach przetwarzanych w czasie rzeczywisty.

Podstawowe kroki programu:

-Odfiltrowywanie kolorów z klatki filmu, tak aby pozostał tylko kolor czerwony

-Wykrywanie koła

-Wycinanie fragmentu z kołem

-Rozpoznawanie cyfr przy pomocy funkcji cv2.matchTemplate()

Aby program działał prawidłowo, należy w folderze src umieścić video, na którym chcemy wykrywać znaki ograniczeń prędkości. Przykładowe filmy z serwisu youtube podane poniżej: 

nazwa: "film1.mp4"
https://www.youtube.com/watch?v=ktnGgSnyhIY&fbclid=IwAR0stg_KWoHOrG_5yx_00W64-ZDoqrZ_kgv8jTUHvYxx_ng6kZLmeo0QLsk

nazwa: "film2.mp4"
https://www.youtube.com/watch?v=N4bM1VxPZUM&fbclid=IwAR2gOt-JnOnT3eaA93bTeI39od_SnO45RXKxB43zxIntNaUdTe-7t2g_dhM

nazwa: "film3.mp4"
https://www.youtube.com/watch?v=BGpNWkjXW5I&fbclid=IwAR23a791fIOFNYBry3YWpVNj8CD16LHq0K5Nhs8nm1OISr31NJD83Lt4WZQ

nazwa: "film4.mp4"
https://www.youtube.com/watch?v=NyPeT5VLUro&fbclid=IwAR0dTfSd_jRY3X5Vs2WJ8ByEmboV5zAbRumDQkLOC9caxcgoF6ZN9XzueFw

Jeżeli program miałby działać dla innych danych, to należy odpowiednio zmdyfikować kod:
#linia 4 - do listy name wpisujemy nazwy filmów, które chcemy przetwarzać
#linia 5- do listy name wpisujemy interesujący nas czas rozpoczęcia dla każdego filmu w milisekundach
#linia 6- do listy name wpisujemy interesujący nas czas zakończenia dla każdego filmu w milisekundach
