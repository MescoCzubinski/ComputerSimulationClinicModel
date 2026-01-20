"""
Moduł przeprowadzający pełną analizę statystyczną symulacji przychodni
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import simulation as sim
import os

OUTPUT_DIR = "results"


def run_multiple_simulations(
        is_scheduled=True,
        runs=100,
        num_registration_desks=2,
        num_doctors=5,
        num_patients=150,
        verbose=True
):
    """
    Przeprowadza wielokrotne symulacje i zbiera surowe dane.
    
    Args:
        is_scheduled: Czy pacjenci mają umówione terminy
        runs: Liczba powtórzeń symulacji
        num_registration_desks: Liczba okienek rejestracji
        num_doctors: Liczba gabinetów
        num_patients: Liczba pacjentów
        verbose: Czy wyświetlać postęp
        
    Returns:
        dict: Słownik z surowymi danymi z symulacji
    """
    avg_times = []
    overtimes = []

    for i in range(runs):
        if is_scheduled:
            result = sim.run_scheduled_simulation(
                num_registration_desks, num_doctors, num_patients
            )
        else:
            result = sim.run_walk_in_simulation(
                num_registration_desks, num_doctors, num_patients
            )

        avg_times.append(result.avg_time)
        overtimes.append(result.overtime)
        
        if verbose and (i + 1) % 10 == 0:
            print(f"Postęp: {int((i + 1) / runs * 100)}%", end='\r')

    return {
        "avg_times": np.array(avg_times),
        "overtimes": np.array(overtimes)
    }


def calculate_statistics(data, name=""):
    """
    Oblicza i zwraca podstawowe statystyki opisowe.
    
    Args:
        data: Tablica danych
        name: Nazwa metryki
        
    Returns:
        dict: Słownik ze statystykami
    """
    return {
        "Metryka": name,
        "Średnia": np.mean(data),
        "Mediana": np.median(data),
        "Odchylenie std": np.std(data),
        "Min": np.min(data),
        "Max": np.max(data),
        "Percentyl 25%": np.percentile(data, 25),
        "Percentyl 75%": np.percentile(data, 75),
        "Percentyl 95%": np.percentile(data, 95),
    }


def z_test(
    data1,
    data2,
    name1="Grupa 1",
    name2="Grupa 2",
    alpha=0.05
):
    """
    Test Z dla dwóch średnich przy znanych wariancjach populacyjnych.

    Args:
        data1, data2 : array-like
            Próby danych
        sigma1, sigma2 : float
            Odchylenia standardowe populacji
        name1, name2 : str
            Nazwy grup
        alpha : float
            Poziom istotności

    Returns:
        dict
    """
    mean1, mean2 = np.mean(data1), np.mean(data2)
    n1, n2 = len(data1), len(data2)
    sigma1 = np.sqrt(np.var(data1, ddof=0))
    sigma2 = np.sqrt(np.var(data2, ddof=0))

    se = np.sqrt((sigma1**2) / n1 + (sigma2**2) / n2)
    z_stat = (mean1 - mean2) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    return {
        f"Średnia {name1}": mean1,
        f"Średnia {name2}": mean2,
        "Różnica średnich": mean1 - mean2,
        "Statystyka Z": z_stat,
        "Wartość p": max(p_value, 1e-16),
        f"Istotne statystycznie (α={alpha})":
            "TAK" if p_value < alpha else "NIE"
    }


def create_histogram_plot(data1, data2, ylabel, title_prefix, filename, 
                          color1='blue', color2='green', add_zero_line=False):
    """
    Tworzy wykres histogramu porównawczy dla dwóch zbiorów danych.
    
    Args:
        data1: Dane dla pierwszego systemu
        data2: Dane dla drugiego systemu
        ylabel: Etykieta osi Y
        title_prefix: Prefix tytułu
        filename: Nazwa pliku do zapisu
        color1: Kolor pierwszego histogramu
        color2: Kolor drugiego histogramu
        add_zero_line: Czy dodać linię na poziomie 0
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    for ax, data, title, color in [
        (ax1, data1, f'{title_prefix} - Z umawianym terminem', color1),
        (ax2, data2, f'{title_prefix} - Bez umawiania terminu', color2)
    ]:
        ax.hist(data, bins=30, alpha=0.7, color=color, edgecolor='black')
        mean_val = np.mean(data)
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, 
                   label=f'Średnia: {mean_val:.2f}')
        if add_zero_line:
            ax.axvline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)
        ax.set_xlabel(ylabel)
        ax.set_ylabel('Częstość')
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=300, bbox_inches='tight')
    plt.close()


def create_comparison_plots(data_scheduled, data_walk_in):
    """
    Tworzy wykresy porównawcze dla obu systemów.
    
    Args:
        data_scheduled: Dane z symulacji z terminami
        data_walk_in: Dane z symulacji bez terminów
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Histogramy średnich czasów pacjentów
    create_histogram_plot(
        data_scheduled["avg_times"], 
        data_walk_in["avg_times"],
        'Średni czas pacjenta (minuty)',
        'Średni czas pacjenta',
        'comparison_avg_patient_time.png'
    )
    
    # Histogramy nadgodzin
    create_histogram_plot(
        data_scheduled["overtimes"], 
        data_walk_in["overtimes"],
        'Nadgodziny (minuty)',
        'Nadgodziny',
        'comparison_overtime.png',
        add_zero_line=True
    )
    
    # Boxploty porównawcze
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1.boxplot([data_scheduled["avg_times"], data_walk_in["avg_times"]], 
                labels=['Z terminem', 'Bez terminu'])
    ax1.set_ylabel('Średni czas pacjenta (minuty)')
    ax1.set_title('Porównanie średniego czasu pacjenta')
    ax1.grid(True, alpha=0.3, axis='y')
    
    ax2.boxplot([data_scheduled["overtimes"], data_walk_in["overtimes"]], 
                labels=['Z terminem', 'Bez terminu'])
    ax2.axhline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    ax2.set_ylabel('Nadgodziny (minuty)')
    ax2.set_title('Porównanie nadgodzin')
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'comparison_boxplots.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\nWykresy porównawcze zapisane w katalogu '{OUTPUT_DIR}/'")


def create_parameter_analysis_plots(results_df, filename='parameter_analysis_patients.png'):
    """
    Tworzy wykresy analizy wpływu liczby pacjentów na wskaźniki.
    
    Args:
        results_df: DataFrame z wynikami dla różnych parametrów
        filename: Nazwa pliku do zapisu
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    for system in results_df['System'].unique():
        data = results_df[results_df['System'] == system]
        ax1.plot(data['num_patients'], data['Średni czas pacjenta (min)'], 
                marker='o', label=system, linewidth=2, markersize=6)
        ax2.plot(data['num_patients'], data['Nadgodziny (min)'], 
                marker='o', label=system, linewidth=2, markersize=6)
    
    ax1.set_xlabel('Liczba pacjentów')
    ax1.set_ylabel('Średni czas pacjenta (minuty)')
    ax1.set_title('Wpływ liczby pacjentów na czas pacjenta (num_doctors=5)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.set_xlabel('Liczba pacjentów')
    ax2.set_ylabel('Nadgodziny (minuty)')
    ax2.set_title('Wpływ liczby pacjentów na nadgodziny (num_doctors=5)')
    ax2.axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Wykresy analizy wpływu pacjentów zapisane w katalogu '{OUTPUT_DIR}/'")


def create_doctors_analysis_plots(results_df):
    """
    Tworzy wykresy analizy wpływu liczby gabinetów na wskaźniki.
    
    Args:
        results_df: DataFrame z wynikami dla różnych liczb gabinetów
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    for system in results_df['System'].unique():
        data = results_df[results_df['System'] == system]
        ax1.plot(data['num_doctors'], data['Średni czas pacjenta (min)'], 
                marker='o', label=system, linewidth=2, markersize=6)
        ax2.plot(data['num_doctors'], data['Nadgodziny (min)'], 
                marker='o', label=system, linewidth=2, markersize=6)
    
    ax1.set_xlabel('Liczba gabinetów')
    ax1.set_ylabel('Średni czas pacjenta (minuty)')
    ax1.set_title('Wpływ liczby gabinetów na czas pacjenta (num_patients=150)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.set_xlabel('Liczba gabinetów')
    ax2.set_ylabel('Nadgodziny (minuty)')
    ax2.set_title('Wpływ liczby gabinetów na nadgodziny (num_patients=150)')
    ax2.axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'parameter_analysis_doctors.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Wykresy analizy wpływu gabinetów zapisane w katalogu '{OUTPUT_DIR}/'")


def run_parameter_sweep_patients(num_runs, patients_range, num_registration_desks, num_doctors):
    """
    Przeprowadza analizę wpływu liczby pacjentów na wskaźniki przy stałej liczbie gabinetów.
    
    Args:
        num_runs: Liczba powtórzeń każdej symulacji
        patients_range: Zakres liczby pacjentów do przetestowania
        num_registration_desks: Liczba okienek rejestracji
        num_doctors: Stała liczba gabinetów
        
    Returns:
        DataFrame: Wyniki analizy parametrów
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("\n" + "=" * 70)
    print("ANALIZA WPŁYWU LICZBY PACJENTÓW")
    print("=" * 70)
    print(f"\nStała liczba gabinetów: {num_doctors}")
    print(f"Zmienna liczba pacjentów: {list(patients_range)}")
    
    results = []
    
    for i, num_patients in enumerate(patients_range):
        print(f"Postęp: {int((i+1)/len(patients_range)*100)}%", end="\r")
        
        for is_scheduled, system_name in [(True, "Z terminem"), (False, "Bez terminu")]:
            data = run_multiple_simulations(
                is_scheduled=is_scheduled,
                runs=num_runs,
                num_registration_desks=num_registration_desks,
                num_doctors=num_doctors,
                num_patients=num_patients,
                verbose=False
            )
            
            results.append({
                "num_doctors": num_doctors,
                "num_patients": num_patients,
                "System": system_name,
                "Średni czas pacjenta (min)": np.mean(data["avg_times"]),
                "Nadgodziny (min)": np.mean(data["overtimes"]),
                "Std czas pacjenta": np.std(data["avg_times"]),
                "Std nadgodziny": np.std(data["overtimes"])
            })
    
    results_df = pd.DataFrame(results)
    results_df.to_csv(os.path.join(OUTPUT_DIR, "analiza_wplyw_pacjentow.csv"), index=False, float_format='%.3f')
    
    print(f"\nZapisano: {os.path.join(OUTPUT_DIR, 'analiza_wplyw_pacjentow.csv')}")

    create_parameter_analysis_plots(results_df, 'parameter_analysis_patients.png')
    
    return results_df


def run_parameter_sweep_doctors(num_runs, doctors_range, num_registration_desks, num_patients):
    """
    Przeprowadza analizę wpływu liczby gabinetów na wskaźniki przy stałej liczbie pacjentów.
    
    Args:
        num_runs: Liczba powtórzeń każdej symulacji
        doctors_range: Zakres liczby gabinetów do przetestowania
        num_registration_desks: Liczba okienek rejestracji
        num_patients: Stała liczba pacjentów
        
    Returns:
        DataFrame: Wyniki analizy parametrów
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("\n" + "=" * 70)
    print("ANALIZA WPŁYWU LICZBY GABINETÓW")
    print("=" * 70)
    print(f"\nStała liczba pacjentów: {num_patients}")
    print(f"Zmienna liczba gabinetów: {list(doctors_range)}")
    
    results = []
    
    for i, num_doctors in enumerate(doctors_range):
        print(f"Postęp: {round((i+1)/len(doctors_range)*100)}%", end="\r")
        
        for is_scheduled, system_name in [(True, "Z terminem"), (False, "Bez terminu")]:
            data = run_multiple_simulations(
                is_scheduled=is_scheduled,
                runs=num_runs,
                num_registration_desks=num_registration_desks,
                num_doctors=num_doctors,
                num_patients=num_patients,
                verbose=False
            )
            
            results.append({
                "num_doctors": num_doctors,
                "num_patients": num_patients,
                "System": system_name,
                "Średni czas pacjenta (min)": np.mean(data["avg_times"]),
                "Nadgodziny (min)": np.mean(data["overtimes"]),
                "Std czas pacjenta": np.std(data["avg_times"]),
                "Std nadgodziny": np.std(data["overtimes"])
            })
    
    results_df = pd.DataFrame(results)
    results_df.to_csv(os.path.join(OUTPUT_DIR, "analiza_wplyw_gabinetow.csv"), index=False, float_format='%.3f')
    
    print(f"\nZapisano: {os.path.join(OUTPUT_DIR, 'analiza_wplyw_gabinetow.csv')}")
    create_doctors_analysis_plots(results_df)
    
    return results_df


def run_full_analysis(
        num_runs=100,
        num_registration_desks=2,
        num_doctors=3,
        num_patients=85,
        patients_range=range(10, 100, 10),
        doctors_range=range(1, 6)
):
    """
    Przeprowadza pełną analizę symulacji i generuje wszystkie wyniki.
    
    Args:
        num_runs: Liczba powtórzeń każdej symulacji
        num_registration_desks: Liczba okienek rejestracji
        num_doctors: Liczba gabinetów (dla głównej analizy)
        num_patients: Liczba pacjentów (dla głównej analizy)
        patients_range: Zakres liczby pacjentów dla analizy parametrów
        doctors_range: Zakres liczby gabinetów dla analizy parametrów
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("=" * 70)
    print("ANALIZA SYMULACJI PRZYCHODNI")
    print("=" * 70)
    print(f"\nParametry symulacji:")
    print(f"  - Liczba powtórzeń: {num_runs}")
    print(f"  - Okienka rejestracji: {num_registration_desks}")
    print(f"  - Liczba gabinetów: {num_doctors}")
    print(f"  - Liczba pacjentów: {num_patients}")
    print()
    
    # Zbieranie surowych danych
    print("\n[1/7] Przeprowadzanie symulacji z umawianym terminem...")
    data_scheduled = run_multiple_simulations(
        is_scheduled=True,
        runs=num_runs,
        num_registration_desks=num_registration_desks,
        num_doctors=num_doctors,
        num_patients=num_patients
    )
    
    print("\n[2/7] Przeprowadzanie symulacji bez umawiania terminu...")
    data_walk_in = run_multiple_simulations(
        is_scheduled=False,
        runs=num_runs,
        num_registration_desks=num_registration_desks,
        num_doctors=num_doctors,
        num_patients=num_patients
    )
    
    # Obliczanie statystyk
    print("\n[3/7] Obliczanie statystyk...")
    
    stats_list = [
        calculate_statistics(data_scheduled["avg_times"], "Średni czas pacjenta - Z terminem"),
        calculate_statistics(data_scheduled["overtimes"], "Nadgodziny - Z terminem"),
        calculate_statistics(data_walk_in["avg_times"], "Średni czas pacjenta - Bez terminu"),
        calculate_statistics(data_walk_in["overtimes"], "Nadgodziny - Bez terminu")
    ]
    
    stats_df = pd.DataFrame(stats_list)
    
    # Testy statystyczne Z
    print("\n[4/7] Przeprowadzanie testów Z...")
    
    z_test_patient_time = z_test(
        data_scheduled["avg_times"],
        data_walk_in["avg_times"],

    )
    
    z_test_overtime = z_test(
        data_scheduled["overtimes"],
        data_walk_in["overtimes"]
    )
    
    z_tests_df = pd.DataFrame([
        {"Metryka": "Średni czas pacjenta", **z_test_patient_time},
        {"Metryka": "Nadgodziny", **z_test_overtime}
    ])
    
    # Przygotowanie tabel
    aggregated_df = pd.DataFrame({
        "System": ["Z terminem", "Bez terminu"],
        "Średni czas pacjenta (min)": [
            np.mean(data_scheduled["avg_times"]),
            np.mean(data_walk_in["avg_times"])
        ],
        "Std czas pacjenta": [
            np.std(data_scheduled["avg_times"]),
            np.std(data_walk_in["avg_times"])
        ],
        "Nadgodziny (min)": [
            np.mean(data_scheduled["overtimes"]),
            np.mean(data_walk_in["overtimes"])
        ],
        "Std nadgodziny": [
            np.std(data_scheduled["overtimes"]),
            np.std(data_walk_in["overtimes"])
        ],
        "Liczba symulacji": [num_runs, num_runs],
        "Liczba gabinetów": [num_doctors, num_doctors],
        "Liczba pacjentów": [num_patients, num_patients]
    })
    
    raw_df = pd.DataFrame({
        "Run": list(range(num_runs)) * 2,
        "System": ["Z terminem"] * num_runs + ["Bez terminu"] * num_runs,
        "Średni_czas_pacjenta": list(data_scheduled["avg_times"]) + list(data_walk_in["avg_times"]),
        "Nadgodziny": list(data_scheduled["overtimes"]) + list(data_walk_in["overtimes"])
    })
    
    # Zapisywanie wyników
    print("\n[5/7] Zapisywanie wyników do plików CSV...")
    
    stats_df.to_csv(os.path.join(OUTPUT_DIR, "statystyki_opisowe.csv"), index=False, float_format='%.3f')
    z_tests_df.to_csv(os.path.join(OUTPUT_DIR, "testy_statystyczne_z.csv"), index=False, float_format='%.6f')
    aggregated_df.to_csv(os.path.join(OUTPUT_DIR, "dane_zagregowane.csv"), index=False, float_format='%.3f')
    raw_df.to_csv(os.path.join(OUTPUT_DIR, "dane_surowe.csv"), index=False, float_format='%.3f')
    
    print(f"\nZapisano pliki CSV w katalogu '{OUTPUT_DIR}/':")
    print("  - statystyki_opisowe.csv")
    print("  - testy_statystyczne_z.csv")
    print("  - dane_zagregowane.csv")
    print("  - dane_surowe.csv")
    
    # Tworzenie wykresów
    print("\n[6/7] Generowanie wykresów porównawczych...")
    create_comparison_plots(data_scheduled, data_walk_in)
    
    # Analiza wpływu parametrów
    print("\n[7/7] Przeprowadzanie analiz wpływu parametrów...")
    run_parameter_sweep_patients(num_runs, patients_range, num_registration_desks, num_doctors)
    run_parameter_sweep_doctors(num_runs, doctors_range, num_registration_desks, num_patients)
    
    # Wyświetlanie podsumowania
    print("\n" + "=" * 70)
    print("PODSUMOWANIE WYNIKÓW")
    print("=" * 70)
    
    print("\nSTATYSTYKI OPISOWE:")
    print(stats_df.to_string(index=False))
    
    print("\n\nTESTY STATYSTYCZNE Z:")
    print(z_tests_df.to_string(index=False))
    
    print("\n\nDANE ZAGREGOWANE:")
    print(aggregated_df.to_string(index=False))
    
    print("\n" + "=" * 70)
    print("WNIOSKI:")
    print("=" * 70)
    
    # Automatyczne wnioski
    if z_test_patient_time["Wartość p"] < 0.05:
        diff = z_test_patient_time["Różnica średnich"]
        winner = "Z terminem" if diff < 0 else "Bez terminu"
        print(f"\n1. Średni czas pacjenta:")
        print(f"   Dla przyjętych parametrów system '{winner}' ISTOTNIE STATYSTYCZNIE skraca czas pacjenta")
        print(f"   (różnica: {abs(diff):.2f} min, p={z_test_patient_time['Wartość p']})")
    else:
        print(f"\n1. Średni czas pacjenta:")
        print(f"   Dla przyjętych parametrów BRAK ISTONIE STATYSTYCZNIE różnicy między systemami")
        print(f"   (p={z_test_patient_time['Wartość p']})")
    
    if z_test_overtime["Wartość p"] < 0.05:
        diff = z_test_overtime["Różnica średnich"]
        winner = "Z terminem" if diff < 0 else "Bez terminu"
        print(f"\n2. Nadgodziny:")
        print(f"   Dla przyjętych parametrów system '{winner}' ma ISTOTNIE STATYSTYCZNIE mniejsze nadgodziny")
        print(f"   (różnica: {abs(diff):.2f} min, p={z_test_overtime['Wartość p']})")
    else:
        print(f"\n2. Nadgodziny:")
        print(f"   Dla przyjętych parametrów BRAK ISTONIE STATYSTYCZNIE różnicy między systemami")
        print(f"   (p={z_test_overtime['Wartość p']})")
    
    print("\n" + "=" * 70)
    print("Analiza zakończona!")
    print("=" * 70)


if __name__ == "__main__":
    np.random.seed(42)
    
    # Pełna analiza z wpływem parametrów
    run_full_analysis(
        num_runs=100,
        num_registration_desks=2,
        num_doctors=5,
        num_patients=150,
        patients_range=range(10, 310, 10),
        doctors_range=range(1, 11)
    )