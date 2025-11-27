# 🏧 ATM CLI Program

A Command Line Interface (CLI) based ATM simulation program built with Python. This program simulates a complete banking system with ATM card features, PIN security, transactions, and security protocols.

## 📋 Table of Contents
- [Features](#-features)
- [Folder Structure](#-folder-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Available Features](#-available-features)
- [Technologies](#-technologies)
- [Development Status](#-development-status)

## ✨ Features

- 💳 **Virtual ATM Card System** - Create and manage digital ATM cards
- 🔐 **PIN Security** - PIN verification with automatic blocking system
- 💰 **Complete Transactions** - Cash withdrawal, transfer, deposit, balance check
- 🏦 **Multi Bank Support** - Supports 5 banks: NovaBank, ByteVault, ProtonPay, FluxFinance, ZenithLedger
- 📊 **Transaction History** - Tracking all banking activities
- 🚫 **Blocking System** - Card automatically blocked after 3 incorrect PIN attempts

## 📁 Folder Structure

```
ENJOY/
├── .venv/                  # Python virtual environment
├── admin/                  # System data folder
│   ├── account.json       # User account database
│   ├── blockedATM.log     # Blocked card logs
│   ├── kodebank.json      # Bank codes for transfers
│   ├── makeacc.py         # Account creation script
│   ├── status.json        # Pending transaction status
│   └── tabungan.json      # Balance & transaction database
├── cardatm/               # ATM card storage
├── holeCard/              # ATM card slot (insert card here)
├── .gitignore
└── main.py                # Main ATM program
```

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or Download this repository**
   ```bash
   git clone <repository-url>
   cd ENJOY
   ```

2. **Create Virtual Environment (Optional but recommended)**
   ```bash
   python -m venv .venv
   
   # Activate virtual environment:
   # Windows:
   .venv\Scripts\activate
   
   # Linux/Mac:
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   # Actually, no external dependencies required!
   # All modules used are Python built-ins
   ```

## 📖 Usage

### 1️⃣ Create a Bank Account

Run the account creation script in the `admin/` folder:

```bash
python admin/makeacc.py
```

Follow the instructions:
- Enter PIN (6 digits)
- Enter Full Name
- Enter Date of Birth (format: DD-MM-YYYY)
- Select Bank (1-5)

**Output:** An ATM card file with a random name will be created in the `cardatm/` folder

### 2️⃣ Insert ATM Card

Move the ATM card file from `cardatm/` folder to `holeCard/` folder:

```bash
# Example (Windows):
move cardatm\CardName.json holeCard\

# Example (Linux/Mac):
mv cardatm/CardName.json holeCard/
```

⚠️ **IMPORTANT:** Only **1 card** is allowed in the `holeCard/` folder. If there are more than 1 card, the system will reject for security reasons.

### 3️⃣ Run the ATM Program

```bash
python main.py
```

Enter the PIN you created during registration.

## 🎯 Available Features

### Currently Available:
- ✅ **Balance Information** - Check account balance
- ✅ **Cash Withdrawal** - Withdraw money from account
- ✅ **Deposit** - Deposit money to account
- ✅ **Transfer** - Send money to other accounts
- ✅ **PIN Verification** - Security with 3-attempt system
- ✅ **Blocking System** - Card automatically blocked after 3 incorrect PIN attempts

### Complete Menu:
1. 100.000 (Quick withdraw)
2. 300.000 (Quick withdraw)
3. 500.000 (Quick withdraw)
4. 1.000.000 (Quick withdraw)
5. BALANCE INFORMATION
6. CUSTOM WITHDRAWAL
7. DEPOSIT
8. TRANSFER
9. QUIT

## 💻 Technologies

- **Python 3.x** - Main programming language
- **JSON** - Simple database for data storage
- **hashlib** - Encryption for security
- **getpass** - Hidden PIN input
- **pathlib** - Portable path management

## 🔄 Development Status

**Status:** 🚧 **MAINTENANCE & DEVELOPMENT**

The program is still under active development. New features are being developed to enhance the functionality of this ATM CLI system.

### Roadmap (Coming Soon):
- 📱 Multi-card support with selection menu
- 📊 Detailed transaction history
- 💱 Currency exchange
- 🔔 Notification system
- 📈 Savings account with interest
- 🎫 Bill payment feature

## 🤝 Contributing

Currently, this program is under personal development. Stay tuned for future updates!

## ⚠️ Disclaimer

This program is a **simulation** for educational purposes. It does not use real money and is not connected to any real banking system.

## 📞 Contact & Support

If you find bugs or have suggestions, please create an issue in this repository.

---

**Thank you for trying ATM CLI Program! 🙏**

*Stay tuned for upcoming updates with more complete and exciting features!*

---

### 📝 License

MIT License - Feel free to use and modify

### 🌟 Show Your Support

If this program is helpful, give it a ⭐ on this repository!