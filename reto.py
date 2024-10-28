dias = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
primer = []
residuos = ['R', 'V', 'B', 'A']
sede_principal_b = []
sede_secundaria_b = []
sede_oficina_b = []
basura_en_almacen = {'R': 0, 'B': 0, 'V': 0, 'A': 0}
arreglo_entrada = []

def seleccionar_dia_inicio():
    while True:
        diai = input("Ingresa la primera letra del día en el que inicia el mes a evaluar (x para miércoles): ").upper()
        if diai not in dias:
            print('Valor no válido.')
            continue
        primer.append(diai)
        return dias.index(diai)

def cant_dias():
    while True:
        try:
            cantd = int(input("Ingresa la cantidad de días que tiene el mes: "))
            if cantd > 31 or cantd < 28:
                print("Cantidad de días no válida.")
                continue
            primer.append(cantd)
            return cantd
        except ValueError:
            print('Valor no válido.')

def dia_evaluar(cantd):
    while True:
        try:
            diae = int(input("Ingrese el día en el que se desea evaluar el centro de acopio: "))
            if diae > cantd or diae < 1:
                print("Día a evaluar no válido.")
                continue
            primer.append(diae)
            return diae
        except ValueError:
            print('Valor no válido.')

def actualizar_arreglo_entrada(basura):
    global arreglo_entrada
    for tipo in residuos:
        cantidad = basura.count(tipo)
        if cantidad > 0:
            arreglo_entrada.append(tipo * cantidad)

def acumular_residuos():
    for residuo in arreglo_entrada:
        tipo = residuo[0]
        cantidad = len(residuo)
        basura_en_almacen[tipo] += cantidad
    arreglo_entrada.clear()

def mostrar_estado_acopio(dia):
    print(f" [{''.join(f'{arreglo_entrada.count(tipo)}{tipo}' for tipo in residuos if arreglo_entrada.count(tipo) > 0)}]")
    print(f" [{''.join(f'{basura_en_almacen[tipo]}{tipo}' for tipo in residuos if basura_en_almacen[tipo] > 0)}]")

def pedir_basura(dia_inicio, cantd, diae):
    print("Si desea omitir un día, ingrese simplemente un 0.")
    print("Si desea finalizar el proceso, ingrese un 1.")
    print('''Recuerde lo siguiente:
    Rojo (R) = Peligroso
    Verde (V) = Biodegradable
    Blanco (B) = Reciclables de Papel
    Azul (A) = Plástico''')

    # Entrada de datos hasta el día de evaluación
    for dia in range(1, diae + 1):
        dia_actual = dias[(dia_inicio + dia - 1) % len(dias)]

        while True:
            basura = input(
                f"Ingrese el tipo de residuo(s) para el día {dia_actual} {dia} (ej. RBAABBV, 0 para omitir o 1 para salir): ").upper()

            if basura == "1":
                print("Proceso detenido por el usuario.")
                return

            if basura == "0":
                print(f"Día {dia} omitido.")
                break

            if all(letra in residuos for letra in basura):
                actualizar_arreglo_entrada(basura)

                if dia % 2 != 0:
                    sede_principal_b.append(basura)
                else:
                    sede_secundaria_b.append(basura)

                if dia % 3 == 0:
                    acumular_residuos()

                break
            else:
                print(
                    "Entrada no válida. Ingrese solo letras que pertenezcan a los tipos de residuos (R, V, B, A), 0 para omitir, o 1 para salir.")

        # Ahora preguntar para la sede de oficina incluso si se omite el día
        if dia_actual in ['M', 'J']:
            while True:
                sf = input(
                    f"Ingrese el tipo de residuo(s) para la sede de oficina el día {dia_actual} {dia} (ej. RBAABBV, 0 para omitir, o 1 para finalizar): ").upper()

                if sf == "1":
                    print("Proceso detenido por el usuario.")
                    return

                if sf == "0":
                    print(f"Día {dia} en la oficina omitido.")
                    break

                if all(letra in residuos for letra in sf):
                    sede_oficina_b.append(sf)
                    actualizar_arreglo_entrada(sf)

                    if dia % 3 == 0:
                        acumular_residuos()

                    break
                else:
                    print(
                        "Entrada no válida. Ingrese solo letras que pertenezcan a los tipos de residuos (R, V, B, A), 0 para omitir o 1 para finalizar.")

    # Permitir ingresar residuos para días posteriores al día evaluado
    while True:
        dia_posterior = int(input(f"Ingrese el día posterior al día evaluado para agregar residuos (0 para salir): "))
        if dia_posterior == 0:
            break

        if dia_posterior <= cantd:
            dia_actual = dias[(dia_inicio + dia_posterior - 1) % len(dias)]

            while True:
                basura = input(
                    f"Ingrese el tipo de residuo(s) para el día {dia_actual} {dia_posterior} (ej. RBAABBV, 0 para omitir o 1 para salir): ").upper()

                if basura == "1":
                    print("Proceso detenido por el usuario.")
                    return

                if basura == "0":
                    print(f"Día {dia_posterior} omitido.")
                    break

                if all(letra in residuos for letra in basura):
                    if dia_posterior % 2 != 0:
                        sede_principal_b.append(basura)
                    else:
                        sede_secundaria_b.append(basura)

                    # Pedir residuos de oficina para días posteriores si son M o J
                    if dia_actual in ['M', 'J']:
                        while True:
                            sf = input(
                                f"Ingrese el tipo de residuo(s) para la sede de oficina el día {dia_actual} {dia_posterior} (ej. RBAABBV, 0 para omitir, o 1 para salir): ").upper()

                            if sf == "1":
                                print("Proceso detenido por el usuario.")
                                return

                            if sf == "0":
                                print(f"Día {dia_posterior} en la oficina omitido.")
                                break

                            if all(letra in residuos for letra in sf):
                                sede_oficina_b.append(sf)
                                break
                            else:
                                print(
                                    "Entrada no válida. Ingrese solo letras que pertenezcan a los tipos de residuos (R, V, B, A), 0 para omitir, o 1 para salir.")
                    break
                else:
                    print(
                        "Entrada no válida. Ingrese solo letras que pertenezcan a los tipos de residuos (R, V, B, A), 0 para omitir, o 1 para salir.")
        else:
            print("Día no válido.")

def main():
    dia_inicio = seleccionar_dia_inicio()
    cantd = cant_dias()
    diae = dia_evaluar(cantd)
    pedir_basura(dia_inicio, cantd, diae)
    print(primer, sede_oficina_b, sede_secundaria_b, sede_principal_b)
    mostrar_estado_acopio(diae)

if __name__ == "__main__":
    main()

