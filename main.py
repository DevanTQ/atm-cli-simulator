import os, time, json, getpass, random, hashlib
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.absolute()

pathkodebank = BASE_DIR / "admin" / "kodebank.json"
pathblocked = BASE_DIR / "admin" / "blockedATM.log"
pathtabungan = BASE_DIR / "admin" / "tabungan.json"
pathstatstarik = BASE_DIR / "admin" / "status.json"
pathaccount = BASE_DIR / "admin" / "account.json"
path_folder_card = BASE_DIR / "holeCard"
path_card_storage = BASE_DIR / "cardatm"

fitur = ["100.000", "300.000", "500.000", "1.000.000", "INFORMASI SALDO", 
         "TARIK TUNAI LAIN", "DEPOSIT", "TRANSFER", "QUIT"]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def date():
    now = datetime.now()
    return now.strftime("%d/%m/%Y, %H:%M:%S")

def print_header(title):
    clear()
    width = 60
    print("╔" + "═" * (width - 2) + "╗")
    print("║" + title.center(width - 2) + "║")
    print("╚" + "═" * (width - 2) + "╝")
    print()

def print_box(message):
    lines = message.split('\n')
    max_length = max(len(line) for line in lines)
    width = max_length + 4
    
    print("┌" + "─" * (width - 2) + "┐")
    for line in lines:
        print("│ " + line.ljust(max_length) + " │")
    print("└" + "─" * (width - 2) + "┘")

def format_currency(amount):
    return f"Rp. {amount:,}".replace(',', '.')

def confirm_transaction():
    print('\n' + '─' * 60)
    print('\n Apakah anda ingin melakukan transaksi lainnya?')
    print('   [Y] Ya    [N] Tidak\n')
    test = input('└─> ').upper()
    if test == 'Y':
        dashboard()
    else:
        clear()
        print_box('✔ Terima kasih telah menggunakan layanan kami\n  Mohon ambil kartu ATM Anda!')
        time.sleep(2)
        exit()

def find_card_file():
    """Mencari file kartu yang valid di folder"""
    try:
        valid_cards = []
        
        if pathaccount.exists():
            with open(pathaccount, 'r') as f:
                accounts = json.load(f)
            
            for card_file in accounts.get("cards", []):
                card_path = path_folder_card / card_file
                if card_path.exists():
                    valid_cards.append(card_path)
        
        if not valid_cards:
            excluded_files = ['kodebank.json', 'blocked.json', 'tabungan.json', 'status.json', 'account.json']
            if path_folder_card.exists():
                for file in path_folder_card.glob("*.json"):
                    if file.name not in excluded_files:
                        try:
                            with open(file, 'r') as f:
                                data = json.load(f)
                            if "Pin" in data and "No Rek" in data and "Name" in data:
                                valid_cards.append(file)
                        except:
                            continue
        
        if len(valid_cards) == 0:
            return None
        elif len(valid_cards) > 1:
            clear()
            print_box(f"[X] TERLALU BANYAK KARTU!\n\n   Ditemukan {len(valid_cards)} kartu di mesin ATM.\n   Mohon keluarkan kartu dan masukkan 1 kartu saja.\n\n   Sistem ATM dihentikan untuk keamanan.")
            time.sleep(4)
            exit()
        
        return valid_cards[0]
    except Exception as e:
        raise Exception(f"Error mencari kartu: {str(e)}")

def load_card_data():
    """Membaca data kartu ATM"""
    try:
        card_path = find_card_file()
        if card_path is None:
            raise Exception("Kartu tidak ditemukan")
        
        with open(card_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"Tidak dapat membaca kartu: {str(e)}")

def saldo():
    print_header("INFORMASI SALDO")
    
    try:
        card_data = load_card_data()
        with open(pathtabungan, 'r') as a:
            data = json.load(a)[card_data["No Rek"]]["for"]["Saldo"]
        
        if data == 0:
            print_box(f"[!]  SALDO ANDA KOSONG!\n\n    Saldo Tersisa: {format_currency(data)}")
        elif data > 0:
            print_box(f"✔  INFORMASI SALDO\n\n    Saldo Tersisa: {format_currency(data)}")
        else:
            print_box(f"[!]  SALDO MINUS!\n\n    Saldo Tersisa: {format_currency(data)}")
        
        time.sleep(3)
    except Exception as e:
        print_box(f"[X] ERROR: Tidak dapat membaca informasi saldo\n    {str(e)}")
        time.sleep(3)
    
    confirm_transaction()
    
def deposit():
    print_header("DEPOSIT")
    
    print("┌─────────────────────────────────────────┐")
    print("│  Masukkan Jumlah Deposit                │")
    print("│  Ketik 'Q' untuk kembali ke menu        │")
    print("└─────────────────────────────────────────┘\n")
    
    try:
        value_input = input('└─> Rp. ').strip().upper()
        
        if value_input == 'Q':
            dashboard()
            return
        
        value = int(value_input)
        
        if value <= 0:
            print_box("[X] Jumlah deposit harus lebih dari 0")
            time.sleep(2)
            deposit()
            return
        
        card_data = load_card_data()
        with open(pathtabungan, "r") as f:
            data = json.load(f)

        data[card_data["No Rek"]]["for"]["Saldo"] += value
        data[card_data["No Rek"]]["for"]["Last Transactions"] = f"Topup/Deposit {value}"
        data[card_data["No Rek"]]["for"]["Date Last Transactions"] = date()

        with open(pathtabungan, "w") as f:
            json.dump(data, f, indent=4)
        
        print('\n' + '─' * 60)
        print_box(f"✔ Transaksi Berhasil!\n\n  Deposit: {format_currency(value)}\n  Waktu: {date()}")
        time.sleep(3)
                                
    except ValueError:
        print_box("[X] Input harus berupa angka!")
        time.sleep(2)
        deposit()
        return
    except Exception as e:
        print_box(f"[X] Kesalahan: {str(e)}")
        time.sleep(2)
        return
                                
    confirm_transaction()
        
def transfer():
    print_header("TRANSFER")
    
    bank_options = {
        "1": "NovaBank",
        "2": "ByteVault",
        "3": "ProtonPay",
        "4": "FluxFinance",
        "5": "ZenithLedger"
    }
    
    print("┌─────────────────────────────────────────┐")
    print("│  PILIH BANK TUJUAN:                     │")
    print("│  [1] NovaBank                           │")
    print("│  [2] ByteVault                          │")
    print("│  [3] ProtonPay                          │")
    print("│  [4] FluxFinance                        │")
    print("│  [5] ZenithLedger                       │")
    print("│  [Q] Kembali ke Menu                    │")
    print("└─────────────────────────────────────────┘\n")
    
    while True:
        pilihan = input("└─> Pilih Bank [1-5/Q]: ").strip().upper()
        if pilihan == 'Q':
            dashboard()
            return
        if pilihan in bank_options:
            namebank = bank_options[pilihan]
            break
        else:
            print("    [X] Pilihan tidak valid!\n")
            continue
    
    try:
        with open(pathkodebank, 'r') as a:
            code = json.load(a)["ATM"][namebank]["KODE"]
    except Exception as e:
        print_box(f"[X] Error membaca kode bank: {str(e)}")
        time.sleep(2)
        dashboard()
        return
    
    kodebnk = input(f"└─> Kode Bank {namebank} (Q=Batal): ").strip()
    
    if kodebnk.upper() == 'Q':
        dashboard()
        return
    
    if kodebnk != code:
        print_box("✖ Kode Bank tidak valid!")
        time.sleep(2)
        transfer()
        return
    
    print("    ✔ Kode Bank benar\n")
    local = input("└─> No. Rekening Tujuan (Q=Batal): ").strip()
    
    if local.upper() == 'Q':
        dashboard()
        return
    
    try:
        with open(pathtabungan, 'r') as f:
            datap = json.load(f)[local]["Pemilik Rek"]
            
        with open(pathtabungan, "r") as l:
            data = json.load(l)
            
        card_data = load_card_data()
    except KeyError:
        print_box("[X] Nomor rekening tidak ditemukan!")
        time.sleep(2)
        transfer()
        return
    except Exception as e:
        print_box(f"[X] Error: {str(e)}")
        time.sleep(2)
        return
    
    print('\n' + '─' * 60)
    print(f"\n[!] Informasi Penerima:")
    print(f"   Nama: {datap}")
    print(f"   No. Rek: {local}")
    print(f"   Bank: {namebank}\n")
    
    raw = input('└─> Lanjutkan? [Y/N]: ').strip().upper()

    if raw != "Y":
        print("    [X] Transfer dibatalkan")
        time.sleep(2)
        dashboard()
        return

    print("\n" + "─" * 60 + "\n")
    
    try:
        current_input = input('└─> Jumlah Transfer (Q=Batal): Rp. ').strip().upper()
        
        if current_input == 'Q':
            dashboard()
            return
        
        current = int(current_input)
        
        if current <= 0:
            print_box("[X] Jumlah transfer harus lebih dari 0")
            time.sleep(2)
            transfer()
            return
            
        if data[card_data["No Rek"]]["for"]["Saldo"] < current:
            print_box("[X] Saldo tidak mencukupi!")
            time.sleep(2)
            dashboard()
            return
            
    except ValueError:
        print_box("[X] Input harus berupa angka!")
        time.sleep(2)
        return

    print(f"\n[!] Transfer: {format_currency(current)}")
    print(f"[!] Kepada: {datap}\n")
    trigger = input('└─> Tekan [Enter] untuk konfirmasi atau [Q] untuk batal: ').strip().upper()

    if trigger == "" or trigger == "ENTER":
        data[card_data["No Rek"]]["for"]["Saldo"] -= current
        data[card_data["No Rek"]]["for"]["Out Money"] += current
        data[card_data["No Rek"]]["for"]["Last Transactions"] = f"Transfer to {datap} - Rp. {current}"
        data[card_data["No Rek"]]["for"]["Date Last Transactions"] = date()
        
        data[card_data["No Rek"]]["Transfer"]["Money"] = f'Rp. {current}'
        data[card_data["No Rek"]]["Transfer"]["To Rek"] = local
        data[card_data["No Rek"]]["Transfer"]["Date"] = date()
        data[card_data["No Rek"]]["Transfer"]["Account"] = datap
        
        data[local]["for"]["Saldo"] += current
        data[local]["for"]["Last Transactions"] = f"Menerima Uang Dari {card_data['Name']} Sebesar {current}"
        data[local]["for"]["Date Last Transactions"] = date()

        with open(pathtabungan, "w") as l:
            json.dump(data, l, indent=4)
        
        print('\n' + '─' * 60)
        print_box(f"✔ Transfer Berhasil!\n\n  Kepada: {datap}\n  Jumlah: {format_currency(current)}\n  Waktu: {date()}")
        time.sleep(4)
        confirm_transaction()
    else:
        print_box("[X] Transfer dibatalkan")
        time.sleep(2)
        dashboard()

def tarikrunai():
    print_header("TARIK TUNAI")
    
    print("┌─────────────────────────────────────────┐")
    print("│  Masukkan Jumlah Penarikan              │")
    print("│  Ketik 'Q' untuk kembali ke menu        │")
    print("└─────────────────────────────────────────┘\n")
    
    try:
        current_input = input('└─> Rp. ').strip().upper()
        
        if current_input == 'Q':
            dashboard()
            return
        
        current = int(current_input)
        
        if current <= 0:
            print_box("[X] Jumlah penarikan harus lebih dari 0")
            time.sleep(2)
            tarikrunai()
            return
        
        with open(pathtabungan, 'r') as n:
            data = json.load(n)
            
        card_data = load_card_data()
        
        if data[card_data["No Rek"]]["for"]["Saldo"] < current:
            print_box("[X] Saldo tidak mencukupi!")
            time.sleep(2)
            dashboard()
            return
            
        url = random.randint(1111111111, 9999999999)
        hashed_url = hashlib.sha256(str(url).encode()).hexdigest()
        
        data[card_data["No Rek"]]["for"]["Saldo"] -= current
        data[card_data["No Rek"]]["for"]["Last Transactions"] = f"Tarik Tunai - Rp. {current}"
        data[card_data["No Rek"]]["for"]["Out Money"] += current
        data[card_data["No Rek"]]["for"]["Date Last Transactions"] = date()
        
        with open(pathtabungan, 'w') as v:
            json.dump(data, v, indent=4)
            
        with open(pathstatstarik, 'r') as j:
            readk = json.load(j)
        
        readk["Status"] = "On"
        readk["Jumlah Uang"] = current
        
        with open(pathstatstarik, 'w') as j:
            json.dump(readk, j, indent=4)
        
        print('\n' + '─' * 60)
        print_box(f"✔ Kode Penarikan Berhasil Dibuat!\n\n  Jumlah: {format_currency(current)}\n  Kode: {hashed_url[:16]}...\n  Waktu: {date()}\n\n  ⚠️  Segera lakukan penarikan!")
        time.sleep(5)

    except ValueError:
        print_box("[X] Input harus berupa angka!")
        time.sleep(2)
        tarikrunai()
        return
    except Exception as e:
        print_box(f"[X] Error: {str(e)}")
        time.sleep(2)
        return
            
    confirm_transaction()
            
def statusTariktunai():
    print_header("⸢[!]  STATUS TARIK TUNAI")
    
    try:
        with open(pathstatstarik, 'r') as j:
            readk = json.load(j)["Jumlah Uang"]
        card_data = load_card_data()
        with open(pathtabungan, "r") as l:
            data = json.load(l)
        with open(pathstatstarik, 'r') as h:
            readz = json.load(h)
    except Exception as e:
        print_box(f"[X] Error membaca data: {str(e)}")
        time.sleep(2)
        dashboard()
        return
    
    print(f"[!] Jumlah Tertunda: {format_currency(readk)}\n")
    print("┌─────────────────────────────────────────┐")
    print("│  [O] Batalkan & Kembalikan Saldo        │")
    print("│  [Q] Kembali ke Menu                    │")
    print("└─────────────────────────────────────────┘\n")
    
    acctions = input('└─> Pilihan: ').upper()
    
    if acctions == "O":
        if "Status Tarik Tunai" in fitur:
            fitur.remove("Status Tarik Tunai")
            
        readz["Status"] = "Off"
        readz["Jumlah Uang"] = 0
        data[card_data["No Rek"]]["for"]["Saldo"] += readk
        data[card_data["No Rek"]]["for"]["Last Transactions"] = f"Pengembalian Uang Tarik Tunai Sebesar Rp. {readk}"
        data[card_data["No Rek"]]["for"]["Date Last Transactions"] = date()
        data[card_data["No Rek"]]["for"]["Out Money"] -= readk
        
        with open(pathtabungan, 'w') as l:
            json.dump(data, l, indent=4)
        with open(pathstatstarik, 'w') as j:
            json.dump(readz, j, indent=4)
        
        print_box(f"✔ Transaksi Dibatalkan\n\n  Saldo dikembalikan: {format_currency(readk)}")
        time.sleep(3)
        confirm_transaction()
                    
    elif acctions == "Q":
        dashboard()
    else:
        print("    [X] Pilihan tidak valid")
        time.sleep(1)
        statusTariktunai()
        
def sandi():
    print_header("[?] VERIFIKASI PIN")
    
    current = 3
    
    try:
        card_data = load_card_data()
    except Exception as e:
        print_box(f"[X] Error membaca data kartu: {str(e)}")
        time.sleep(2)
        exit()
    
    print("┌─────────────────────────────────────────┐")
    print("│  Masukkan PIN ATM Anda                  │")
    print(f"│  Sisa Percobaan: {current}                        │")
    print("└─────────────────────────────────────────┘\n")
    
    while True:
        value = getpass.getpass(prompt="└─> PIN: ").strip()
        
        if value == card_data["Pin"]:
            print("\n    ✔ PIN Benar")
            time.sleep(1)
            break
        else:
            current -= 1
            if current < 1:
                print_box("[X] KARTU DIBLOKIR!\n\n   Anda telah salah memasukkan PIN 3 kali.\n   Hubungi bank untuk membuka blokir.")
                with open(pathblocked, 'a') as a:
                    a.write(f'{card_data["No Rek"]}\n')
                time.sleep(3)
                exit()

            print(f"\n    [X] PIN Salah! Sisa percobaan: {current}\n")
            time.sleep(1)

def dashboard():
    lock = []
    
    try:
        card_data = load_card_data()
        lock.append(card_data["No Rek"])
    except Exception as e:
        print_box(f"[X] Error: Kartu tidak dapat dibaca\n    {str(e)}")
        time.sleep(2)
        exit()
        
    try:
        with open(pathstatstarik, 'r') as h:
            readz = json.load(h)
    except:
        readz = {"Status": "Off"}
    
    while True:
        print_header("ATM SYSTEM")
        
        print("┌─────────────────────────────────────────┐")
        print("│  Memverifikasi Kartu...                 │")
        print("└─────────────────────────────────────────┘\n")
        
        if readz.get("Status") == "On" and "Status Tarik Tunai" not in fitur:
            fitur.append("Status Tarik Tunai")
        
        card_file = find_card_file()
        if card_file is None:
            print("    [!]  Masukkan kartu ATM Anda!")
            time.sleep(3)
            continue
        
        time.sleep(1)
        
        is_blocked = False
        if os.path.exists(pathblocked):
            with open(pathblocked, 'r') as bf:
                blocked_lines = [line.strip() for line in bf if line.strip()]
            if any(item in blocked_lines for item in lock):
                is_blocked = True

        if is_blocked:
            clear()
            print_box("[X] KARTU DIBLOKIR!\n\n   Hubungi pihak bank untuk informasi lebih lanjut.\n   Customer Service: 1500-xxx")
            time.sleep(3)
            exit()
        
        sandi()
        
        print_header("[!] MENU UTAMA [!]")
        
        print("┌─────────────────────────────────────────┐")
        for i, item in enumerate(fitur, start=1):
            print(f"│  {i}. {item.ljust(37)}│")
        print("└─────────────────────────────────────────┘\n")
        
        tindakan = input("└─> Pilih menu: ").strip()
        
        if tindakan == "5":
            saldo()
        elif tindakan == "6":
            tarikrunai()
        elif tindakan == "7":
            deposit()
        elif tindakan == "8":
            transfer()
        elif tindakan == "9":
            clear()
            print_box("✔ Terima kasih!\n\n  Mohon ambil kartu ATM Anda")
            time.sleep(2)
            exit()
        elif tindakan == "10" and "Status Tarik Tunai" in fitur:
            statusTariktunai()
        else:
            print("\n    [X] Pilihan tidak valid!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        dashboard()
    except KeyboardInterrupt:
        clear()
        print_box("[!]  Sesi dibatalkan\n\n  Mohon ambil kartu ATM Anda")
        time.sleep(2)
    except Exception as e:
        clear()
        print_box(f"[X] Error sistem:\n   {str(e)}\n\n  Hubungi administrator")
        time.sleep(3)