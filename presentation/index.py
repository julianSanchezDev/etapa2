from business.admin import Verifier, UserManager, ApiController, business_helper
from decimal import Decimal
import bcrypt
from getpass import getpass

class App:
    def __init__(self):
        self.dni = ''
        self.password = ''
        self.user_manager = UserManager()
        self.logged_in = False
        self.api_controller = None

    def Run(self):
        print("Bienvenidos a la app de consultas")
        while True:
            print("Seleccionar opción:")
            print("1) Iniciar sesión")
            print("2) Crear Usuario")
            print("3) Modificar Password")
            opcion = input("Por favor seleccionar una opción (1-3): ")

            if opcion == '1':
                self.IniciarSesion()
                break

            elif opcion == '2':
                self.NuevoUsuario()
                break

            elif opcion == '3':
                self.ModificarPassword()
                break

            else:
                print("Opción inválida. Por favor, seleccionar una opción válida.")

    def IniciarSesion(self):
        self.dni = input("Por favor ingrese su usuario: ")
        self.password = getpass("Ingrese su contraseña: ")
        print('Su usuario es: ' + self.dni)

        self.password = self.password.lower()

        myVerifier = Verifier(self.dni, self.password)

        try:
            if myVerifier.Verify():
                self.logged_in = myVerifier.logged_in
                self.api_controller = ApiController(username=self.dni)

        except Exception as e:
            print(e.args[0])
            self.logged_in = False

        if self.logged_in:
            self.AgregarFondos()
            self.RealizarCompra()

    def AgregarFondos(self):
        verifier = Verifier(self.dni, self.password)

        if verifier.Verify():
            myadmin = business_helper(username=verifier.dni)
            try:
                saldo_ars = myadmin.data_helper.getAccountBalance("ARS", myadmin.username)
                if saldo_ars == "0.00" or input("Desea agregar fondos a su billetera en pesos ARGENTINOS? (S/N): ").lower() == "s":
                    print("Ingrese la cantidad de dinero a agregar a su billetera en pesos ARGENTINOS:")
                    amount_ars = input()
                    myadmin.addFunds("ARS", amount_ars)
                    print("Se han agregado fondos a su billetera en pesos ARGENTINOS")
            except Exception as e:
                print(e.args[0])
        else:
            print("No es necesario agregar fondos a su billetera, ya que está comprando en pesos ARS.")

    def RealizarCompra(self):
        verifier = Verifier(self.dni, self.password)

        if verifier.Verify():
            myadmin = business_helper(username=verifier.dni)
            saldo_ars = myadmin.data_helper.getAccountBalance("ARS", myadmin.username)
            if saldo_ars == "0.00":
                print("No tiene fondos en pesos ARS. Por favor, agregue fondos antes de realizar una compra.")
                return

            moneda_comprar, cantidad_comprar, cantidad_peso = self.api_controller.procesar_transaccion()
            print("****** DETALLES DE COMPRA ******:")
            print("Tipo de moneda a comprar:", moneda_comprar)
            print("Cantidad a comprar:", cantidad_comprar)
            print("Cantidad en pesos argentinos:", cantidad_peso)

            try:
                # Verificar si hay suficientes fondos en pesos ARS
                if Decimal(saldo_ars) < Decimal(cantidad_peso):
                    print("No tiene suficientes fondos en su Billetera de pesos ARS.")
                    return

                # Solicitar la cantidad a comprar en la moneda seleccionada por usuario
                while True:
                    try:
                        nueva_cantidad_comprar = Decimal(input("Ingrese la cantidad de {} que desea comprar: ".format(moneda_comprar)))
                        if nueva_cantidad_comprar != cantidad_comprar:
                            print("La cantidad NO COINCIDEN. Por favor, ingrese la misma cantidad nuevamente.")
                        else:
                            cantidad_comprar = nueva_cantidad_comprar

                            # Restar los fondos en pesos ARS
                            if moneda_comprar != "ARS":
                                try:
                                    myadmin.data_helper.subtractFunds("ARS", myadmin.username, cantidad_peso)
                                    print("Se han restado fondos de su cuenta en pesos ARS.")
                                except Exception as e:
                                    print(e.args[0])

                            # Agregar fondos a la billetera en la moneda de compra
                            myadmin.addFunds(moneda_comprar, cantidad_comprar)
                            print("Se han agregado fondos a su billetera en", moneda_comprar)

                            break
                    except ValueError:
                        print("Error: cantidad inválida. Ingrese un número válido.")

            except Exception as e:
                print(e.args[0])
        else:
            print("No es necesario agregar fondos a su billetera, ya que está comprando en pesos ARS.")






#Crear Nuevo Usuario
    def NuevoUsuario(self):
        dni = input("Escriba su nombre de USUARIO: ")
        password = getpass("Enter Password: ")
        cpassword = getpass("Repetir Password: ")

        if self.user_manager.create_user(dni, password, cpassword):
            encrypted_name = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            hashed_password = bcrypt.hashpw(cpassword.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            self.user_manager.data_helper.saveCredentials(self.dni, encrypted_name, hashed_password)
        else:
            print("No se puede crear el usuario debido a errores en los datos ingresados.")
#Modificar password
    def ModificarPassword(self):
        self.dni = input("Ingrese el USUARIO: ")
        self.password = getpass("Ingrese la contraseña actual: ")

        verified, _ = self.user_manager.verifyCredentials(self.dni, self.password)

        if verified:
            new_password = getpass("Ingrese la nueva contraseña: ")

            if self.user_manager.modifyPassword(self.dni, self.password, new_password):
                print("Contraseña modificada exitosamente.")
            else:
                print("No se encontró el USUARIO especificado.")
        else:
            print("Credenciales incorrectas.")