import pandas as pd
import requests
import json
import hashlib
from datetime import datetime
from conn import conn, sysdate

def principal(test = None):
    print("Bienvenido, abajo digite el país a buscar, recuerde que escribiendo salir o terminar recibira la tabla final")

    proceso = True
    i = 0
    listaData = []
    while proceso:
        name = input("Digite nombre del pais a buscar: ")
        if ("terminar" in name) or ("salir" in name):
            break
        now = str(datetime.now())
        url = "https://restcountries.com/v2/name/" + name

        data = requests.get(url)
        if data.status_code == 200:
            data = json.loads(data.text)
            data = data[0]

            pais = data["name"]
            region = data["region"]
            idioma = data["languages"][0]["nativeName"]

            byte = str(idioma).encode()
            hash_object = hashlib.sha1(byte)
            pbHash = hash_object.hexdigest()

            list = [region, pais, pbHash]
        else:
            list = ["No encontrado", name, ""]

        
        then = str(datetime.now())

        date_format_str = '%Y-%m-%d %H:%M:%S.%f'

        start = datetime.strptime(now, date_format_str)
        end =   datetime.strptime(then, date_format_str)

        diff = end - start

        diffMS = diff.total_seconds() * 1000
        diffMS = float(format(diffMS, '.2f'))
        
        list.append(diffMS)
        listaData.append(list)
        i += 1

    if i == 0:
        print("No hay tabla final para mostrar")
        return "No hay tabla final para mostrar"
    else:
        dataFrame = pd.DataFrame(listaData, columns=["Region", "City Name","Language", "Time"])
        max = str(dataFrame["Time"].max()) + " ms"
        min = str(dataFrame["Time"].min()) + " ms"
        sum = str(dataFrame["Time"].sum()) + " ms"
        avg = str(dataFrame["Time"].mean()) + " ms"
        if test:
            return dataFrame
        index = dataFrame.index
        for i in index:
            dataFrame.loc[i, "Time"] = str(dataFrame.iloc[i]["Time"])+ " ms"
        print("========================================================================")
        print(dataFrame)
        print("========================================================================")
        print("Tiempo maximo: ", max)
        print("Tiempo minimo: ", min)
        print("Tiempo total: ", sum)
        print("Tiempo promedio: ", avg)
        
        datos = {}
        for i in index:
            dato = {
                "Region": dataFrame.iloc[i]["Region"],
                "City_Name": dataFrame.iloc[i]["City Name"],
                "Language": dataFrame.iloc[i]["Language"],
                "Time": dataFrame.iloc[i]["Time"]
            }
            datos[i] = dato
        
        fecha = sysdate()
        nombreArchivo = "data" + fecha + ".json"
        datos = json.dumps(datos)
        archivo = open("json/" + nombreArchivo, "w")
        archivo.write(datos)
        archivo.close()

        conexion = conn()
        nombreTabla = "Paises" + "_" + fecha
        dataFrame.to_sql(name=nombreTabla, con=conexion)
        conexion.close()
        return dataFrame


if __name__ == "__main__":
   principal()