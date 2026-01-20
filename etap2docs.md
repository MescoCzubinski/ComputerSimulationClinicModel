# Dokumentacja projektu przychodni

## Struktura plików
- `distributions.py` – generowanie rozkładów czasów przyjścia, rejestracji i wizyt oraz list pacjentów.
- `simulation.py` – rdzeń symulacji przepływu pacjentów oraz funkcje uruchamiające scenariusze.
- `main.py` – prosty punkt wejścia wypisujący winiki obu wariantów przychodni.

## Generatory rozkładów (`distributions.py`)
- `get_walk_in_arrival_time_dist(num_patients, p_first=0.5)`  
  Dwumodalny rozkład normalny czasów przyjścia dla pacjentów bez zapisu (piki ok. 9:00 i 14:00). Wyniki ograniczane do godzin pracy przychodni.
- `get_arrival_offset(num_patients)`  
  Asymetryczny rozkład normalny przesunięć względem terminu wizyty (średnio -10 minut, prawostronny ogon) dla pacjentów umówionych.
- `get_scheduled_arrival_time_dist(num_patients, num_doctors)`  
  Tworzy czasy przyjścia co 20 minut na gabinet, z dodanym przesunięciem z powyższego rozkładu.
- `get_registration_duration_dist(num_patients, multiplier)`  
  Czas rejestracji z rozkładu wykładniczego, skalowany mnożnikiem (dłuższa rejestracja dla pacjentów niezapowiedzianych).
- `get_appointment_duration_dist(num_patients)`  
  Czas trwania wizyty z rozkładu gamma (średnio 17 minut, zawsze >0).
- `get_scheduled_patients(num_patients, num_doctors)`  
  Zwraca posortowaną listę pacjentów z umówionymi terminami: `(czas_przyjścia, czas_rejestracji, czas_wizyty)`.
- `get_run_walk_in_patients(num_patients)`  
  Zwraca posortowaną listę pacjentów przychodzących bez zapisu.

## Rdzeń symulacji (`simulation.py`)
- `SimulationResult`  
  Prosty agregat wyników: średni łączny czas pacjenta (`avg_time`), łączny czas bezczynności lekarzy (`idle_time`), listy czasów pobytu i oczekiwania na lekarza oraz bezczynność per lekarz (`idle_times`).
- `ClinicSimulation`  
  Symuluje przepływ pacjentów:
  - rejestracja: pacjent wybiera pierwsze wolne okienko, oczekuje lub zaczyna od razu;
  - gabinet: pacjent wybiera pierwszego wolnego lekarza, bezczynność lekarza jest sumowana;
  - metryki: zapisywany jest czas całkowity (przybycie → koniec wizyty) oraz czas oczekiwania na lekarza.
- `run_scheduled_simulation(num_registration_desks=2, num_doctors=3, num_patients=100)`  
  Uruchamia symulację dla pacjentów z terminami umówionymi i zwraca `SimulationResult`.
- `run_walk_in_simulation(num_registration_desks=2, num_doctors=3, num_patients=100)`  
  Uruchamia symulację dla pacjentów przychodzących z ulicy i zwraca `SimulationResult`.

## Uruchamianie
```bash
python main.py
```
Przed uruchomieniem można zmienić parametry wywołań `run_scheduled_simulation` oraz `run_walk_in_simulation` w `main.py`, aby sprawdzić inne konfiguracje liczby gabinetów, okienek rejestracji lub pacjentów.
