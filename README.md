1. Skład osobowy zespołu:
- Jan Guziak (284028),
- Eryk Boczula (284018),
- Mieszko Czubiński (284047).

2. Temat projektu:
porównanie dwóch sposobów organizacji przychodni

3. Parametry:
Deterministyczne:
- Liczba okienek rejestracji (int, 1-3)
- Liczba gabinetów (int, 1-10)
- Liczbę pacjentów (int, 1-300)

Losowe:
- W przypadku pacjentów przychodzących z ulicy: lista pacjentów - czyli krotek z:
  - czasem przyjścia (datetime, z dokładnością do 1 minuty, rozkład: bimodalny z wartościami maksymalnymi w godzinach 9. i 14.),
  - czas spędzony w rejestracji (rozkład wykładniczy),
  - czas trwania wizyty (rozkład gamma).

- W przypadku pacjentów przychodzących na umówiony termin: lista pacjentów - czyli krotek z:
  - czasem przyjścia (datetime, co 20 minut z przesunięciem o liczbę minut z asymetrycznego rozkładu normalnego z wartością oczekiwaną -10 minut i ogonem prawostronnym),
  - czas spędzony w rejestracji (potwierdzenie rejestracji) (rozkład wykładniczy),
  - czas trwania wizyty (rozkład gamma).

4. Opis:
System jest przychodnią z podaną przez nas liczbą gabinetów i okienek rejestracji (parametry deterministyczne). Do przychodni przychodzą pacjenci. Analizujemy dwa sposoby organizacji wizyt:
- Z umawianiem terminu (pacjenci mają zaplanowane wizyty na konkretne godziny). Popularny przypadek znany z wielu przychodni.
- Bez umawiania terminu (pacjenci przychodzą w dowolnym momencie). Przypadek stosowany w przychodniach nocnych.

Pacjent po przyjściu do przychodni ustawia się w kolejce do rejestracji (w przypadku pacjentów z umówionym terminem rejestracja jest jedynie potwierdzeniem przybycia). Po zarejestrowaniu wizyty ustawia się w kolejce do gabinetu. Wychodzi po zakończeniu wizyty, której czas jest zależny od wylosowanego wcześniej czasu trwania.

Wskaźniki oceny systemu:
- średni czas spędzony przez pacjenta w przychodni, od przybycia do zakończenia wizyty,
- łączny czas bezczynności gabinetów.

Hipotezy:
- Przychodnia z umawianym terminem skraca czas spędzony przez pacjenta w przychodni,
- Sposób organizacji kolejek wpływa na łączny czas bezczynności gabinetu.

Cel:
Porównanie przychodni w zależności od sposobu umawiania pacjentów dla danej liczby okienek i gabinetów.

5. Narzędzie:
- python,
- SimPy
