import json, hashlib, base64, os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.absolute()

if BASE_DIR.name == "admin":
    PROJECT_ROOT = BASE_DIR.parent
else:
    PROJECT_ROOT = BASE_DIR

path_tabungan = PROJECT_ROOT / "admin" / "tabungan.json"
path_card_storage = PROJECT_ROOT / "cardatm"
path_account = PROJECT_ROOT / "admin" / "account.json"
# ======================================

def hash_pendek(teks, panjang=10):
    h = hashlib.sha256(teks.encode()).digest()
    b = base64.b64encode(h).decode()
    return b[:panjang]

def generate_no_rek(name, bank, tgl_lahir, panjang=10):
    kombinasi = f"{name}{bank}{tgl_lahir}"
    return hash_pendek(kombinasi, panjang)

def date():
    now = datetime.now()
    return now.strftime("%d/%m/%Y, %H:%M:%S")

def input_data_akun():
    print("\n=== INPUT DATA AKUN BANK ===")
    
    pin = input("Masukkan Pin (6 digit): ").strip()
    name = input("Masukkan Nama: ").strip()
    tgl_lahir = input("Masukkan Tanggal Lahir (contoh: 15-08-1995): ").strip()
    
    valid_banks = {
        "1": "NovaBank",
        "2": "ByteVault",
        "3": "ProtonPay",
        "4": "FluxFinance",
        "5": "ZenithLedger"
    }
    
    print("\n┌─────────────────────────────────────────┐")
    print("│  PILIH BANK:                            │")
    print("│  [1] NovaBank                           │")
    print("│  [2] ByteVault                          │")
    print("│  [3] ProtonPay                          │")
    print("│  [4] FluxFinance                        │")
    print("│  [5] ZenithLedger                       │")
    print("└─────────────────────────────────────────┘\n")
    
    while True:
        pilihan = input("└─> Pilih Bank [1-5]: ").strip()
        if pilihan in valid_banks:
            bank = valid_banks[pilihan]
            break
        else:
            print("    [X] Pilihan tidak valid! Pilih angka 1-5\n")
    
    no_rek = generate_no_rek(name, bank, tgl_lahir)
    print(f"\n✔ No Rek otomatis: {no_rek}")
    
    return {
        "Pin": pin,
        "Name": name,
        "Tanggal Lahir": tgl_lahir,
        "Bank": bank,
        "No Rek": no_rek
    }

def update_account_json(nama_file_card):
    """Update atau buat file account.json untuk tracking kartu"""
    try:
        if path_account.exists():
            with open(path_account, 'r', encoding='utf-8') as f:
                account_data = json.load(f)
        else:
            account_data = {"cards": []}
        
        if nama_file_card not in account_data.get("cards", []):
            if "cards" not in account_data:
                account_data["cards"] = []
            account_data["cards"].append(nama_file_card)
        
        with open(path_account, 'w', encoding='utf-8') as f:
            json.dump(account_data, f, indent=4, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"[X] Error update account.json: {e}")
        return False

def buat_akun_bank():
    print("=" * 50)
    print("GENERATOR AKUN BANK")
    print("=" * 50)
    
    admin_folder = PROJECT_ROOT / "admin"
    if not admin_folder.exists():
        try:
            admin_folder.mkdir(parents=True, exist_ok=True)
            print(f"✔ Folder 'admin' berhasil dibuat")
        except Exception as e:
            print(f"[X] Error membuat folder admin: {e}")
            return
    
    if not path_card_storage.exists():
        try:
            path_card_storage.mkdir(parents=True, exist_ok=True)
            print(f"✔ Folder 'cardatm' berhasil dibuat")
        except Exception as e:
            print(f"[X] Error membuat folder cardatm: {e}")
            return
    
    hole_card_folder = PROJECT_ROOT / "holeCard"
    if not hole_card_folder.exists():
        try:
            hole_card_folder.mkdir(parents=True, exist_ok=True)
            print(f"✔ Folder 'holeCard' berhasil dibuat")
        except Exception as e:
            print(f"[X] Error membuat folder holeCard: {e}")
    
    data_akun = input_data_akun()
    
    nama_file_card = f"{hash_pendek(data_akun['Name'], 10)}.json"
    file_path_card = path_card_storage / nama_file_card
    
    data_tabungan_entry = {
        data_akun["No Rek"]: {
            "Pemilik Rek": data_akun["Name"],
            "Bank": data_akun["Bank"],
            "for": {
                "Saldo": 0,
                "Out Money": 0,
                "Last Transactions": "",
                "Date Last Transactions": ""
            },
            "Transfer": {
                "Money": "",
                "To Rek": "",
                "Date": "",
                "Account": ""
            }
        }
    }
    
    data_card = {
        "Pin": data_akun["Pin"],
        "Name": data_akun["Name"],
        "Tanggal Lahir": data_akun["Tanggal Lahir"],
        "Bank": data_akun["Bank"],
        "No Rek": data_akun["No Rek"]
    }
    
    try:
        if path_tabungan.exists():
            with open(path_tabungan, 'r', encoding='utf-8') as f:
                data_tabungan = json.load(f)
        else:
            data_tabungan = {}
        
        if data_akun["No Rek"] in data_tabungan:
            print(f"\n[X] Akun dengan No Rek {data_akun['No Rek']} sudah ada!")
            return
        
        data_tabungan.update(data_tabungan_entry)
        
        with open(path_tabungan, 'w', encoding='utf-8') as f:
            json.dump(data_tabungan, f, indent=4, ensure_ascii=False)
        
        with open(file_path_card, 'w', encoding='utf-8') as f:
            json.dump(data_card, f, indent=4, ensure_ascii=False)
        
        update_account_json(nama_file_card)
        
        print("\n" + "=" * 50)
        print("✔ AKUN BANK BERHASIL DIBUAT!")
        print("=" * 50)
        print(f"\n[INFORMASI AKUN]")
        print(f"Nama         : {data_akun['Name']}")
        print(f"Bank         : {data_akun['Bank']}")
        print(f"No Rekening  : {data_akun['No Rek']}")
        print(f"Tanggal Lahir: {data_akun['Tanggal Lahir']}")
        print(f"\n[STATUS]")
        print(f"✔ Data akun berhasil disimpan ke: {path_tabungan}")
        print(f"✔ File kartu ATM berhasil dibuat: {nama_file_card}")
        print(f"✔ Tracking kartu berhasil ditambahkan ke: {path_account}")
        print(f"\n[!] CARA MENGGUNAKAN KARTU:")
        print(f"    1. Copy file kartu '{nama_file_card}' dari folder 'cardatm'")
        print(f"    2. Paste ke folder 'holeCard'")
        print(f"    3. Jalankan main.py untuk menggunakan kartu!")
        print(f"\n[LOKASI FILE]")
        print(f"Kartu: {file_path_card}")
        
    except Exception as e:
        print(f"\n[X] Error menyimpan file: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    buat_akun_bank()