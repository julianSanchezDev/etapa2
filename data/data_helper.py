import bcrypt
import json
from os import path
from currencies import curr
from decimal import Decimal



class DataHelper:
    def __init__(self):
        self.filepath = 'userdata.json'

    def matchNameDni(self, dni, password):
        if path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                data = json.load(f)
                if dni in data:
                    stored_password = data[dni]["password"]
                    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                        return dni, data[dni]["name"]
                    else:
                        return dni, None
        return None, None

    def saveCredentials(self, dni, password, cpassword):
        encrypted_name = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        hashed_password = bcrypt.hashpw(cpassword.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        data = {}
        if path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                data = json.load(f)

        data[dni] = {
            "name": encrypted_name,
            "password": hashed_password
        }

        with open(self.filepath, "w") as f:
            json.dump(data, f)

    def modifyPassword(self, dni, new_password):
        if path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                data = json.load(f)
                if dni in data:
                    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                    data[dni]["password"] = hashed_password.decode('utf-8')

                    with open(self.filepath, "w") as f:
                        json.dump(data, f)
                    return True

        return False


class data_helper:

    def checkAccounts(self, username):
        filename = username + ".json"
        if path.exists(filename):
            if self.AccountExist("ARS", username):
                return True
            else:
                return False
        with open(filename, "w") as f:
            account_des = {"ARS": "0.00"}
            account_ser = json.dumps(account_des, indent=4)
            f.write(account_ser)
        return True

    def isCurrCodeValid(self, currCode):
        if currCode in curr.keys():
            return True
        return False

    def AccountExist(self, currCode, username):
        filename = username + ".json"
        with open(filename, "r") as f:
            file_content = f.read()
            file_des = json.loads(file_content)
            if currCode in file_des.keys():
                return True
            else:
                return False

    def createAccount(self, curr_code, username):
        filename = username + ".json"
        accounts_des = {}
        with open(filename, "r") as f:
            file_content = f.read()
            accounts_des = json.loads(file_content)
        accounts_des.update({curr_code: "0.00"})
        with open(filename, "w") as f:
            accounts_ser = json.dumps(accounts_des, indent=4)
            f.write(accounts_ser)

    def addFunds(self, curr_code, username, amount):
        filename = username + ".json"
        with open(filename, "r") as f:
            file_content = f.read()
            accounts_des = json.loads(file_content)
        if curr_code in accounts_des:
            current_balance = Decimal(accounts_des[curr_code])
            new_balance = current_balance + Decimal(amount)
            accounts_des[curr_code] = str(new_balance)
            with open(filename, "w") as f:
                accounts_ser = json.dumps(accounts_des, indent=4)
                f.write(accounts_ser)
            return True
        else:
            return False
    def getAccountBalance(self, curr_code, username):
        filename = username + ".json"
        with open(filename, "r") as f:
            file_content = f.read()
            accounts_des = json.loads(file_content)
        if curr_code in accounts_des:
            return accounts_des[curr_code]
        else:
            return "0.00"
        
    def subtractFunds(self, curr_code, username, amount):
        filename = username + ".json"
        with open(filename, "r") as f:
            file_content = f.read()
            accounts_des = json.loads(file_content)
        if curr_code in accounts_des:
            current_balance = Decimal(accounts_des[curr_code])
            new_balance = current_balance - Decimal(amount)
            if new_balance < 0:
                raise Exception("No hay suficientes fondos en la cuenta.")
            accounts_des[curr_code] = str(new_balance)
            with open(filename, "w") as f:
                accounts_ser = json.dumps(accounts_des, indent=4)
                f.write(accounts_ser)
            return True
        else:
            return False

