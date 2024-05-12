from pruebas.model.chi2_test import ChiTest

passed_data = []


def fastTest(ri_numbers):

    global passed_data

    passed_data.clear()

    all_data = ri_numbers.copy()
    num_passedTwo = 0  # Inicializar contador de datos pasados

    num_iterations = len(ri_numbers) // 1000
    for i in range(num_iterations):
        start_index = i * 1000
        end_index = (i + 1) * 1000

        subset_data = all_data[start_index:end_index]

        ri_numbers = subset_data

        test = ChiTest(subset_data)
        
        if test.checkTest():
            for value in subset_data:
                passed_data.append(value)
        # Actualizar contador de datos pasados
        num_passedTwo += len(subset_data)
    if len(passed_data) > 0:
        num_passedOne = len(passed_data)
        print(f"Estado de la prueba: Pasaron {num_passedOne/1000} grupos de 1000 de {num_passedTwo/1000} grupos de 1000 Datos")
    else:
        print(f"Estado de la prueba: El set de datos no pasó la prueba de Chi2")


def getPassedData():
    return passed_data