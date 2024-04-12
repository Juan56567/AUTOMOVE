import shutil
import os


papelera = "C:/Users/juan/Dropbox/Aplicaciones/Kizeo Forms/A PAPELERA"
path = os.path.join("\\", "Users", "juan", "Dropbox", "Aplicaciones", "Kizeo Forms")
matriz = os.path.join(
    "\\", "Users", "juan", "Dropbox", "03. PRODUCCION ORDEN DE TRABAJO"
)

listaOdt = os.listdir(matriz)
folders = {}

for i in listaOdt:
    odt = "".join(x for x in i if x.isdigit())
    odt = odt[:4]
    ruta = "C:" + matriz + "\\" + i
    diagnosticos = ruta + "\\REGISTRO FOTOGRAFICO\\1. DIAGNOSTICO"
    reparaciones = ruta + "\\REGISTRO FOTOGRAFICO\\2. REPARACIÓN"
    if os.path.exists(diagnosticos) and os.path.exists(reparaciones):
        fotosDiag = len(os.listdir(diagnosticos))
        fotosRep = len(os.listdir(reparaciones))
        folders.update(
            {
                odt: {
                    "ruta": ruta,
                    "diagnosticos": diagnosticos,
                    "reparaciones": reparaciones,
                    "fotosDiag": fotosDiag,
                    "fotosRep": fotosRep,
                }
            }
        )

listaKizeo = os.listdir(path)
dictKizeo = {}

for i in listaKizeo:
    odt = i[:4]
    try:
        reparado = i.split("-")
        reparado = reparado[2]
        ruta = os.path.join(path, i)
        files = [os.path.join(path, i, x) for x in os.listdir(os.path.join(path, i))]
    except Exception as e:
        pass
    if len(files) == 0:
        rutaCarpetaVacia = os.path.join(path, i)
        shutil.move(rutaCarpetaVacia, papelera)
    else:
        dictKizeo.update({odt: {"ruta": ruta, "reparado": reparado, "files": files}})


for i in dictKizeo:
    try:
        if i in folders:
            dataDest = folders[i]
            diagDestino = dataDest["fotosDiag"]
            repDestino = dataDest["fotosRep"]
            rutaDiagDestino = dataDest["diagnosticos"]
            rutaRepDestino = dataDest["reparaciones"]
            repOrigen = dictKizeo[i]["reparado"].upper()
            cantidadFotosOrigen = len(dictKizeo[i]["files"])

            if repOrigen == "SÍ" and cantidadFotosOrigen > repDestino:
                for x in dictKizeo[i]["files"]:
                    shutil.move(x, rutaRepDestino)
                print("Se movieron fotos de reparación de la ODT", i)

            elif repOrigen == "SÍ" and cantidadFotosOrigen <= repDestino:
                print("Ya tiene fotos de reparacion ODT ", i)
                shutil.move(dictKizeo[i]["ruta"], papelera)

            elif repOrigen == "NO" and cantidadFotosOrigen > diagDestino:
                for x in dictKizeo[i]["files"]:
                    shutil.move(x, rutaDiagDestino)
                print("Se movieron fotos de diagnóstico de la ODT", i)

            elif repOrigen == "NO" and cantidadFotosOrigen <= diagDestino:
                print("Ya tienen fotos de diagnostico la ODT: ", i, dictKizeo[i])
                shutil.move(dictKizeo[i]["ruta"], papelera)

            else:
                print("nada", i)

    except Exception as e:
        print(e)


for i in listaKizeo:
    odt = i[:4]
    try:
        reparado = i.split("-")
        reparado = reparado[2]
        files = [os.path.join(path, i, x) for x in os.listdir(os.path.join(path, i))]
        ruta = os.path.join(path, i)
    except Exception as e:
        pass
    if len(files) == 0:
        rutaCarpetaVacia = os.path.join(path, i)
        shutil.move(rutaCarpetaVacia, papelera)
    else:
        dictKizeo.update({odt: {"reparado": reparado, "files": files}})
