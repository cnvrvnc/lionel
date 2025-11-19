def hitung_pangkat(bilangan):
    """Menghitung kuadrat dan kubik dari sebuah bilangan."""

    kuadrat = bilangan ** 2  # Pangkat 2
    kubik = bilangan ** 3    # Pangkat 3

    return kuadrat, kubik

# --- Penggunaan Program ---

# Input
try:
    angka = float(input("Masukkan sebuah bilangan: "))

    # Panggil fungsi
    hasil_kuadrat, hasil_kubik = hitung_pangkat(angka)

    # Output
    print(f"\n--- Hasil Pangkat dari {angka:.2f} ---")
    print(f"Kuadrat (Pangkat 2): {hasil_kuadrat:.2f}")
    print(f"Kubik (Pangkat 3): {hasil_kubik:.2f}")

except ValueError:
    print("Input tidak valid. Harap masukkan bilangan.")
