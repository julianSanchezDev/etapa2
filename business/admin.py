from data.data_helper import DataHelper, data_helper
from fixer import ManagerApi


class Verifier:
    def __init__(self, dni, password):
        self.dni = dni
        self.password = password
        self.logged_in = False

    def Verify(self):
        myDataHelper = DataHelper()
        rdni, rpassword = myDataHelper.matchNameDni(self.dni, self.password)
        if rdni is None:
            raise Exception("No se encontró el usuario")
        elif rpassword is None:
            raise Exception("Error en la contraseña")
        else:
            self.logged_in = True
            return True


class business_helper:
    def __init__(self, username):
        self.username = username
        self.logged = True
        self.data_helper = data_helper()
        if not self.data_helper.checkAccounts(self.username):
            raise Exception("Formato de Datos inadecuado")

    def createAccount(self, curr_code, username):
        curr_code = curr_code.lstrip().rstrip().upper()
        if not self.data_helper.isCurrCodeValid(curr_code):
            raise Exception("Codigo de moneda no valido")
        if self.data_helper.AccountExist(curr_code, username):
            raise Exception("Ya Existe la cuenta que desea crear")
        self.data_helper.createAccount(curr_code, username)

    def addFunds(self, curr_code, amount):
        if self.data_helper.addFunds(curr_code, self.username, amount):
            raise Exception("Dinero agregado a la billetera exitosamente.")
        else:
            raise Exception("Error al agregar dinero a la billetera.")

    def getAccountBalance(self, curr_code):
        return self.data_helper.getAccountBalance(curr_code, self.username)


class UserManager:
    def __init__(self):
        self.data_helper = DataHelper()

    def create_user(self, dni, name, password):
        if name == password:
            try:
                self.data_helper.saveCredentials(dni, name, password)
                print("Usuario creado exitosamente")
                return True
            except Exception as e:
                print("Error al crear el usuario:", str(e))
        else:
            raise Exception("El nombre y su repetición no coinciden. No se puede crear el usuario.")
        return False

    def delete_user(self, dni, password):
        try:
            self.data_helper.deleteCredentials(dni, password)
            print("Usuario borrado exitosamente")
        except Exception as e:
            print("Error al borrar el usuario:", str(e))

    def verifyCredentials(self, dni, password):
        result_dni, result_name = self.data_helper.matchNameDni(dni, password)

        if result_dni:
            return True, result_name
        else:
            return False, None

    def modifyPassword(self, dni, old_password, new_password):
        result, _ = self.verifyCredentials(dni, old_password)

        if result:
            if self.data_helper.modifyPassword(dni, new_password):
                return True
            else:
                return False
        else:
            return False


class ApiController:
    def __init__(self, username):
        self.username = username
        self.manager = ManagerApi()

    def procesar_transaccion(self):
        moneda_comprar, cantidad_comprar = self.manager.obtener_moneda_cantidad()
        cantidad_peso = self.manager.calcular_equivalente(moneda_comprar, cantidad_comprar, self.username)
        return moneda_comprar, cantidad_comprar, cantidad_peso

    def agregar_fondos(self, curr_code, amount):
        try:
            myadmin = business_helper(username=self.username)
            myadmin.createAccount(curr_code, self.username)
            myadmin.addFunds(curr_code, amount)
            print("Dinero agregado a la billetera exitosamente.")

            if curr_code != "ARS":
                # Realizar la conversión a ARS
                ars_amount = self.manager.convertir_a_ars(curr_code, amount, self.username)
                if ars_amount is not None:
                    myadmin.addFunds("ARS", ars_amount)
                    print("Fondos convertidos a ARS y agregados a la billetera.")
                else:
                    print("No se pudo realizar la conversión a ARS.")

        except Exception as e:
            print(e.args[0])
