# Sugerencias para proximas versiones:
    # - Función 'Unir': permitir al usuario seleccionar el orden de los archivos PDF a unir 
                        # y seleccionar los mismos desde carpetas no necesariamente iguales.

import PyPDF2
import tkinter as tk
from tkinter import filedialog, simpledialog
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem
from PIL import Image
from pdf2image import convert_from_path

# Crear la ventana principal
root = tk.Tk()

def unir_pdfs():
    # Aquí va el código para unir archivos PDF
    # Obtener los archivos PDF que deseas unir
    archivos = filedialog.askopenfilenames(title="Selecciona los archivos PDF que deseas unir",
                                        filetypes=[("Archivos PDF", "*.pdf")])

    # Crear un objeto PDFMerger
    unidor_pdf = PyPDF2.PdfMerger()

    # Agregar los archivos a unir
    archivos_abiertos = []
    for archivo in archivos:
        f = open(archivo, 'rb')
        unidor_pdf.append(f)
        archivos_abiertos.append(f)

    # Crear un nuevo archivo PDF y escribir los archivos unidos
    archivo_unido = filedialog.asksaveasfile(title="Guardar archivo unido como", defaultextension=".pdf",
                                            filetypes=[("Archivos PDF", "*.pdf")], mode='wb')
    unidor_pdf.write(archivo_unido)

    # Cerrar los archivos
    for f in archivos_abiertos:
        f.close()
    archivo_unido.close()
    pass

def extraer_paginas():
    # Aquí va el código para extraer páginas de un archivo PDF

    # Pedir al usuario que ingrese el rango de páginas a extraer
    rango_paginas = simpledialog.askstring("Extraer páginas", "Ingresa el rango de páginas a extraer (por ejemplo, 1-3,10-11)")

    # Procesar el rango de páginas ingresado por el usuario
    paginas = []
    for rango in rango_paginas.split(","):
        if "-" in rango:
            inicio, fin = map(int, rango.split("-"))
            paginas.extend(range(inicio, fin+1))
        else:
            paginas.append(int(rango))

    # Pedir al usuario que seleccione el archivo PDF de origen
    archivo_origen = filedialog.askopenfilename(title="Selecciona el archivo PDF de origen",
                                                filetypes=[("Archivos PDF", "*.pdf")])

    # Crear un objeto PdfFileReader para leer el archivo PDF de origen
    lector_pdf = PyPDF2.PdfReader(open(archivo_origen, 'rb'))

    # Crear un objeto PdfFileWriter para escribir el nuevo archivo PDF
    escritor_pdf = PyPDF2.PdfWriter()

    # Agregar las páginas especificadas al nuevo archivo PDF
    for pagina in paginas:
        escritor_pdf.add_page(lector_pdf.pages[pagina-1])

    # Pedir al usuario que seleccione el archivo PDF de destino
    archivo_destino = filedialog.asksaveasfile(title="Guardar archivo PDF como", defaultextension=".pdf",
                                               filetypes=[("Archivos PDF", "*.pdf")], mode='wb')

    # Escribir el nuevo archivo PDF
    escritor_pdf.write(archivo_destino)

    # Cerrar los archivos
    archivo_destino.close()
    pass

def reordenar_paginas():
        # Aquí va el código para reordenar las páginas de un archivo PDF
    class PdfReorder(QMainWindow):
        def __init__(self):
            super().__init__()

            # Set the window title
            self.setWindowTitle("Reorder PDF Pages")

            # Create the list widget to display the page thumbnails
            self.list_widget = QListWidget()
            self.list_widget.setIconSize(QtCore.QSize(124, 175))
            self.list_widget.setDragDropMode(QListWidget.InternalMove)
            self.setCentralWidget(self.list_widget)

            # Create the menu bar
            menu_bar = self.menuBar()
            file_menu = menu_bar.addMenu("File")

            # Create the open action
            open_action = QtWidgets.QAction("Open", self)
            open_action.triggered.connect(self.open_pdf)
            file_menu.addAction(open_action)

            # Create the save action
            save_action = QtWidgets.QAction("Save", self)
            save_action.triggered.connect(self.save_pdf)
            file_menu.addAction(save_action)

        def open_pdf(self):
            # Get the input PDF file
            input_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
            if not input_file:
                return

            # Read the input PDF file
            self.pdf_reader = PyPDF2.PdfReader(input_file)

            # Clear the list widget
            self.list_widget.clear()

            # Convert the PDF pages to images
            images = convert_from_path(input_file)

            # Add the page thumbnails to the list widget
            for i, image in enumerate(images):
                image.thumbnail((124, 175), Image.Resampling.LANCZOS)
                qimage = QtGui.QImage(image.tobytes("raw", "RGB"), image.width, image.height, QtGui.QImage.Format_RGB888)
                icon = QtGui.QIcon(QtGui.QPixmap.fromImage(qimage))
                item = QListWidgetItem(icon, f"Page {i + 1}")
                self.list_widget.addItem(item)

        def save_pdf(self):
            # Create the output PDF file
            pdf_writer = PyPDF2.PdfWriter()

            # Get the new page order from the list widget
            for i in range(self.list_widget.count()):
                page_text = self.list_widget.item(i).text()
                page_number = int(page_text.split()[-1]) - 1
                pdf_writer.add_page(self.pdf_reader.pages[page_number])

            # Save the output PDF file
            output_file, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
            if not output_file:
                return

            with open(output_file, "wb") as f:
                pdf_writer.write(f)

    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = PdfReorder()
        window.show()
        sys.exit(app.exec_())
    pass

def rotar_paginas():

    angle = simpledialog.askstring("Ángulo","Indique el ángulo de rotación (horario)")
    angle = int(angle)

    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

    pdf_in = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_in)
    pdf_writer = PyPDF2.PdfWriter()

    for pagenum in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[pagenum]
        page.rotate(angle)
        pdf_writer.add_page(page)

    save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if save_path:
        with open(save_path, 'wb') as f:
            pdf_writer.write(f)

    pdf_in.close()
    pass

# Crear botones para cada opción
boton_unir = tk.Button(root, text="Unir PDFs", command=unir_pdfs)
boton_extraer = tk.Button(root, text="Extraer páginas", command=extraer_paginas)
boton_reordenar = tk.Button(root, text="Reordenar páginas", command=reordenar_paginas)
boton_rotar = tk.Button(root, text="Rotar páginas", command=rotar_paginas)

# Colocar los botones en la ventana
boton_unir.pack()
boton_extraer.pack()
boton_reordenar.pack()
boton_rotar.pack()

# Ejecutar la ventana principal
root.mainloop()

