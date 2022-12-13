# Bitcoin Multisig-Backup
A quick program in Python to create a nice printable backup for a bitcoin 2/3 multisig wallet.

## Instructions for use on Linux
1. Make a new folder on your computer.
2. Open up a terminal in that new folder.
3. Git clone this repository.
```
git clone https://github.com/EverydayBitcoiner/multisig-backup.git
```
4. Create a virtual environment.
```
virtualenv multisig-backup-venv
```
5. Activate virtualenv.
```
source multisig-backup-venv/bin/activate
```
6. Navigate into the repo folder.
```
cd multisig-backup
```
7. Install required dependencies.
```
pip install -r requirements.txt
```
8. Run the program.
```
python create_backup_cards.py
```
9. Input desired multisig wallet name, wallet descriptor, and qr density as prompted.
Note: Be sure to get the full wallet descriptor from sparrow by clicking the edit button shown on the far right in the image below, this will bring up a pop-up box with the full text of the descriptor which can then be copied and pasted into the command line:
![image](https://user-images.githubusercontent.com/119913286/207154432-4c0313fd-1fb1-472d-a196-fa9c09206175.png)

10. Print out the resulting pdf file that will be located in the same folder.
11. Add seed phrase by hand after printing out.
12. Store each care safely and securely, you will need at least 2 of the cards to access/recover your wallet.

Here is an example output:
[Multisig_Backup_multi_sig_backup.pdf](https://github.com/EverydayBitcoiner/multisig-backup/files/10212925/Multisig_Backup_multi_sig_backup.pdf)
