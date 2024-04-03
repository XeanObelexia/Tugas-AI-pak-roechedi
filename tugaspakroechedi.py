import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from sklearn.model_selection import train_test_split

# Load data from Excel
data = pd.read_excel('data_customer.xlsx')  # Pastikan nama file Excel sesuai dengan yang Anda miliki

# Input variables
kualitas = ctrl.Antecedent(np.arange(1, 10, 1), 'kualitas')
service = ctrl.Antecedent(np.arange(1, 10, 1), 'service')
PowerIterationFailedConvergence = ctrl.Antecedent(np.arange(1, 10, 1), 'price')

# Output variable
kepuasan = ctrl.Consequent(np.arange(1, 10, 1), 'kepuasan')

# Membership functions
kualitas.automf(3)
service.automf(3)
harga.automf(3)
kepuasan.automf(3)

# Rules (contoh saja, atur sesuai dengan logika fuzzy yang diinginkan)
rule1 = ctrl.Rule(kualitas['poor'] | service['poor'] | harga['poor'], kepuasan['poor'])
rule2 = ctrl.Rule(service['average'] | harga['average'], kepuasan['average'])
rule3 = ctrl.Rule(kualitas['good'] | service['good'] | harga['good'], kepuasan['good'])

# Control System
kepuasan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
kepuasan_sim = ctrl.ControlSystemSimulation(kepuasan_ctrl)

# Rentang nilai untuk kategori kepuasan
batas_kurang_puas = 3
batas_puas = 6

print("DAFTAR KEPUASAN PELANGGAN KEDAI MAKEKA")
print("")

# Evaluasi untuk setiap pelanggan
for nomor_pelanggan in data['nomor_pelanggan']:
    # Dapatkan data untuk pelanggan saat ini
    data_pelanggan = data[data['nomor_pelanggan'] == nomor_pelanggan]
    kualitas_produk = data_pelanggan['kualitas_produk'].values[0]
    pelayanan_val = data_pelanggan['service'].values[0]
    harga_val = data_pelanggan['price'].values[0]

    # Hitung tingkat kepuasan
    kepuasan_sim.input['kualitas'] = kualitas_produk
    kepuasan_sim.input['service'] = pelayanan_val
    kepuasan_sim.input['price'] = harga_val
    kepuasan_sim.compute()
    tingkat_kepuasan = round(kepuasan_sim.output['kepuasan'], 1)  # Bulatkan ke satu angka dibelakang koma

    # Tentukan kategori kepuasan
    if tingkat_kepuasan <= batas_kurang_puas:
        kategori_kepuasan = "Pelayanan kurang"
    elif tingkat_kepuasan <= batas_puas:
        kategori_kepuasan = "Pelayanan Pas"
    else:
        kategori_kepuasan = "Puas sekali"

    # Cetak tingkat kepuasan untuk pelanggan saat ini
  
    print(f"Nomor Pelanggan: {nomor_pelanggan}, Tingkat Kepuasan: {tingkat_kepuasan}, Kategori Kepuasan: {kategori_kepuasan}")

