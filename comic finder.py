#aplicacion para descargar imagenes


import tkinter as tk
import _thread
import requests as rq
from tkinter import filedialog
import os
import os.path
import re

class prog():
    def __init__(self):
        self.main = tk.Tk(className='buscador')
        self.main.geometry('400x300')

        StrEnum = 'enumerar (enumera las imagenes)'
        self.EnumOption = tk.IntVar()

        self.EntryFolder = tk.Entry(self.main)
        self.EntryFolder.insert(0,'C:/')

        self.ButtonFolder = tk.Button(
                                      self.main,
                                      text='cambiar',
                                      command=self.cambiar_folder
                                      )

        self.LabelUrl = tk.Label(
                                 self.main,
                                 text='URL'
                                 )
        self.EntryUrl = tk.Entry(self.main)
        self.LabelEstado = tk.Label(
                                    self.main,
                                    text='estado'
                                    )
        self.LabelDescarga = tk.Label(
                                      self.main,
                                      text='descargas'
                                      )
        self.ChckbttnEnumerar = tk.Checkbutton(
                                               self.main,
                                               text=StrEnum,
                                               variable=self.EnumOption,
                                               onvalue=1,offvalue=0
                                               )
        self.ButtonBuscar = tk.Button(
                                      self.main,
                                      text='buscar',
                            	      command=lambda:_thread.start_new_thread(
                                          self.buscador,
                                          (None,)
                                          )
				      )
        self.ButtonAyuda = tk.Button(
                                     self.main,
                                     text='ayuda'
                                     )

        self.EntryFolder.pack()
        self.ButtonFolder.pack()
        self.LabelUrl.pack()
        self.EntryUrl.pack()
        self.LabelEstado.pack()
        self.LabelDescarga.pack()
        self.ChckbttnEnumerar.pack()
        self.ButtonBuscar.pack()
        self.ButtonAyuda.pack()
        
        self.main.mainloop()


    def cambiar_folder(self):#fución simple para cambiar la carpeta que recibe
        nueva_carpeta = tk.filedialog.askdirectory()#la descarga
        self.EntryFolder.delete(0,tk.END)
        self.EntryFolder.insert(0,nueva_carpeta)

    def buscador(self,a):
        self.LabelEstado['text'] = 'inicio'
        self.LabelDescarga['text'] = 'buscando imagenes'

        if not os.path.exists(self.EntryFolder.get()):#crea la carpeta
            os.makedirs(self.EntryFolder.get())#receptora si es que no existe

        imagenes_a_descargar = self.EntryUrl.get()

        try:
            imagenes_a_descargar = rq.get(imagenes_a_descargar).text
            print(imagenes_a_descargar)
            imagenes_a_descargar = self.extractor(imagenes_a_descargar)#extrae
            self.LabelDescarga['text'] = 'aqui' 
        except rq.exceptions.ConnectionError:#las url de imagenes del codigo en
            self.LabelEstado['text'] = 'no hay interntet'#HTML en la función
                                                        #extractor
        print(imagenes_a_descargar)
        self.descargador(imagenes_a_descargar)#Descarga las imagenes de las url
        self.LabelEstado['text'] = 'Listo'#a traves de la función descargador
        self.LabelDescarga['text'] = 'descargas'

    def extractor(self, source_code):#extraer los links de las fotos
        source_code = re.findall(r'(http[^\s"]+(.jpg|.jpeg|.png|.tiff)\b)', source_code)
        self.LabelEstado['text'] = 'imagenes encontradas'
        return source_code

    def descargador(self,source_code):
        for num,i in enumerate(source_code[:]):
            if self.EnumOption.get():
                dir_imagen = self.descarga_a(num,i)
            else:
                dir_imagen = self.descarga_b(i)

            if os.path.isfile(dir_imagen):
                self.LabelEstado['text'] = 'saltando'
                self.LabelDescarga['text'] = 'descargando {}\n{}/{}'.format\
                                        (i,num,len(source_code))
                continue
            self.LabelDescarga['text'] = 'descargando {}\n{}/{}'.format\
                                    (i,num,len(source_code))
            imagen = rq.get(i[0]).content            
            self.LabelEstado['text'] = 'descargando'
            with open(dir_imagen,'wb+') as f:
                f.write(imagen)
            num = num+1

    def descarga_a(self,numero,i):
        x = '{}/imagen_{:03d}.{}'.format\
            (self.EntryFolder.get(),numero,i[-1])
        return x

    def descarga_b(self,url):
        if len(self.EntryFolder.get()) == 3:
            return self.EntryFolder.get()+url.split("/")[-1]
        return self.EntryFolder.get()+'/'+url.split("/")[-1]
if __name__ == '__main__':
    a = prog()
