# Dokumentacja projektu przychodni

## Struktura plików

- `distributions.py` – generowanie rozkładów czasów przyjścia, rejestracji i wizyt oraz list pacjentów.
- `simulation.py` – rdzeń symulacji przepływu pacjentów oraz funkcje uruchamiające scenariusze.
- `main.py` – prosty punkt wejścia wypisujący wyniki obu wariantów przychodni.
- `analysis.py` – moduł analizy statystycznej przeprowadzający wielokrotne symulacje, testy statystyczne i generujący wykresy.

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
  Prosty agregat wyników: średni łączny czas pacjenta (`avg_time`), nadgodziny (`overtime`), listy czasów pobytu i oczekiwania na lekarza oraz bezczynność per lekarz (`idle_times`). Nadgodziny ujemne oznaczają wcześniejsze zakończenie pracy, dodatnie - pracę po godzinach.
- `ClinicSimulation`  
  Symuluje przepływ pacjentów:
    - rejestracja: pacjent wybiera pierwsze wolne okienko, oczekuje lub zaczyna od razu;
    - gabinet: pacjent wybiera pierwszego wolnego lekarza, bezczynność lekarza jest sumowana;
    - metryki: zapisywany jest czas całkowity (przybycie → koniec wizyty) oraz czas oczekiwania na lekarza.
- `run_scheduled_simulation(num_registration_desks=2, num_doctors=3, num_patients=100)`  
  Uruchamia symulację dla pacjentów z terminami umówionymi i zwraca `SimulationResult`.
- `run_walk_in_simulation(num_registration_desks=2, num_doctors=3, num_patients=100)`  
  Uruchamia symulację dla pacjentów przychodzących z ulicy i zwraca `SimulationResult`.

## Analiza statystyczna (`analysis.py`)

- `run_multiple_simulations(is_scheduled=True, runs=100, num_registration_desks=2, num_doctors=3, num_patients=85, verbose=True)`  
  Przeprowadza wielokrotne symulacje i zbiera surowe dane: średnie czasy pacjentów oraz nadgodziny.

- `run_full_analysis(num_runs=100, num_registration_desks=2, num_doctors=3, num_patients=85, patients_range=range(10, 100, 10), doctors_range=range(1, 6))`  
  Główna funkcja przeprowadzająca pełną analizę

- `calculate_statistics(data, name="")`  
  Oblicza podstawowe statystyki opisowe dla podanego zbioru danych: średnią, medianę, odchylenie standardowe, minimum, maksimum oraz percentyle (25%, 75%, 95%). Zwraca słownik ze statystykami.

- `z_test(data1, data2, name1="Z terminem", name2="Bez terminu", alpha=0.05)`  
  Przeprowadza test Z dla dwóch niezależnych próbek. Oblicza statystykę Z, wartość p (test dwustronny) oraz sprawdza istotność statystyczną przy α=0.05. Zwraca słownik z wynikami testu.

- `create_histogram_plot(data1, data2, ylabel, title_prefix, filename, color1='blue', color2='green', add_zero_line=False)`  
  Uniwersalna funkcja tworząca histogram porównawczy dla dwóch zbiorów danych (system z terminami vs bez terminów). Opcjonalnie dodaje linię odniesienia na poziomie 0 (dla nadgodzin).

- `create_comparison_plots(data_scheduled, data_walk_in)`  
  Tworzy komplet wykresów porównawczych:
    - Histogramy średnich czasów pacjentów dla obu systemów
    - Histogramy nadgodzin dla obu systemów (z linią odniesienia y=0)
    - Boxploty porównawcze dla obu metryk

- `create_parameter_analysis_plots(results_df, filename='parameter_analysis_patients.png')`  
  Tworzy wykresy liniowe pokazujące wpływ liczby pacjentów na:
    - Średni czas pacjenta
    - Nadgodziny

- `create_doctors_analysis_plots(results_df)`  
  Tworzy wykresy liniowe pokazujące wpływ liczby gabinetów na:
    - Średni czas pacjenta
    - Nadgodziny

- `run_parameter_sweep_patients(num_runs, patients_range, num_registration_desks, num_doctors)`  
  Analizuje wpływ liczby pacjentów na wskaźniki przy stałej liczbie gabinetów. Testuje różne liczby pacjentów i dla każdej uruchamia `num_runs` symulacji obu systemów. Wyniki zapisuje do `analiza_wplyw_pacjentow.csv` i generuje odpowiednie wykresy.

- `run_parameter_sweep_doctors(num_runs, doctors_range, num_registration_desks, num_patients)`  
  Analizuje wpływ liczby gabinetów na wskaźniki przy stałej liczbie pacjentów. Testuje różne liczby gabinetów i dla każdej uruchamia `num_runs` symulacji obu systemów. Wyniki zapisuje do `analiza_wplyw_gabinetow.csv` i generuje odpowiednie wykresy.

### Pliki wyjściowe

Moduł `analysis.py` generuje następujące pliki w katalogu `results/`:

**CSV:**

- `statystyki_opisowe.csv` - statystyki dla obu systemów (średnia, mediana, std, percentyle)
- `testy_statystyczne_z.csv` - wyniki testów Z porównujących oba systemy
- `dane_zagregowane.csv` - podsumowanie wyników (średnie, odchylenia standardowe)
- `dane_surowe.csv` - wszystkie surowe wyniki z poszczególnych przebiegów symulacji
- `analiza_wplyw_pacjentow.csv` - wpływ liczby pacjentów na wskaźniki
- `analiza_wplyw_gabinetow.csv` - wpływ liczby gabinetów na wskaźniki

**Wykresy (PNG):**

- `comparison_avg_patient_time.png` - histogramy średniego czasu pacjenta
- `comparison_overtime.png` - histogramy nadgodzin
- `comparison_boxplots.png` - boxploty obu metryk
- `parameter_analysis_patients.png` - wykresy wpływu liczby pacjentów
- `parameter_analysis_doctors.png` - wykresy wpływu liczby gabinetów

## Uruchamianie

### Podstawowa symulacja

```bash
python main.py
```

Przed uruchomieniem można zmienić parametry wywołań `run_scheduled_simulation` oraz `run_walk_in_simulation` w `main.py`, aby sprawdzić inne konfiguracje liczby gabinetów, okienek rejestracji lub pacjentów.

### Analiza statystyczna

```bash
python analysis.py
```

Uruchamia pełną analizę z domyślnymi parametrami:

- 100 powtórzeń każdej symulacji
- 2 okienka rejestracji
- 5 gabinetów (dla głównej analizy)
- 150 pacjentów (dla głównej analizy)
- Testy wpływu liczby pacjentów: (10, 20, 30, ..., 300)
- Testy wpływu liczby gabinetów: (1, 2, 3, ..., 10)

Parametry można zmienić edytując wywołanie `run_full_analysis()` w sekcji `if __name__ == "__main__":`.
