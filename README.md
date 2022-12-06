# Bitcoin Multisig-Backup
A quick program in Python to create a nice printable backup for a bitcoin multisig backup.

## Instructions for use on Linux
1. Make a new folder on your computer.
2. Open up a terminal in that new folder.
3. Git clone this repository.
```
git clone https://github.com/EverydayBitcoiner/multisig-backup.git
```
5. Create a virtual environment.
```
virtualenv multisig-backup-venv
```
7. Activate virtualenv.
```
source multisig-backup-venv/bin/activate
```
9. Install required dependencies.
```
pip install -r requirements.txt
```
11. Run the program.
```
python create_backup_cards.py
```
13. Input desired multisig wallet name, wallet descriptor, and qr density as prompted.
14. Print out the resulting pdf file that will be located in the same folder.
15. Add seed phrase by hand after printing out.
16. Store each care safely and securely, you will need at least 2 of the cards to access/recover your wallet.

