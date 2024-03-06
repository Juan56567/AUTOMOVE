import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import os


matriz = os.path.join(
    "\\", "Users", "Lenovo", "Dropbox", "03. PRODUCCION ORDEN DE TRABAJO"
)
papelera = "C:/Users/Lenovo/Dropbox/Aplicaciones/Kizeo Forms/A PAPELERA"



path = os.path.join("\\", "Users", "Lenovo", "Dropbox", "Aplicaciones", "Kizeo Forms")
matriz = os.path.join(
    "\\", "Users", "Lenovo", "Dropbox", "03. PRODUCCION ORDEN DE TRABAJO"
)


nuevasCarpetas = {}


def on_created(event):
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
    ruta = "C:" + event.src_path
    odt = "".join(i for i in ruta if i.isdigit())
    folderName = os.path.basename(ruta)
    ruta = os.path.join(path, folderName)
    reparado = folderName.split("-")[2].strip().upper()
    data = folders[odt]
    print(
        f"Waiting for images {odt}, fixed {reparado}, diag photos: {data['fotosDiag']} , fix photos : {data['fotosRep']}"
    )
    time.sleep(200)
    fotos = [os.path.join(ruta, f) for f in os.listdir(ruta)]
    print(f"Moving {odt} fixed {reparado}")
    if reparado == "NO" and data["fotosDiag"] == 0:
        for i in fotos:
            shutil.move(i, data["diagnosticos"])
    elif reparado == "SÍ" and data["fotosRep"] == 0:
        for i in fotos:
            shutil.move(i, data["reparaciones"])
    else:
        for i in fotos:
            os.remove(i)


if __name__ == "__main__":

    event_handler = FileSystemEventHandler()
    event_handler.on_created = on_created
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print(f"start watching directory {path!r}")
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
