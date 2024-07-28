import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

class FaunaFloraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Fauna y Flora")
        self.root.configure(bg='#f0f0f0')  # Color de fondo de la ventana
        self.connection = self.create_connection()
        
        # Crear los widgets de la interfaz
        self.create_widgets()
        
    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Asegúrate de poner la contraseña correcta aquí
                database="semana8"  # Asegúrate de que el nombre de la base de datos no tenga espacios
            )
            if connection.is_connected():
                print("Conexión exitosa a la base de datos.")
                return connection
        except Error as e:
            messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
            self.root.destroy()
            return None
    
    def create_widgets(self):
        # Etiquetas y campos de entrada
        self.labels = ['ID', 'Nombre Científico', 'Hábitat', 'Estado de Conservación', 'Región Geográfica']
        self.entries = {}
        for idx, label in enumerate(self.labels):
            ttk.Label(self.root, text=label, background='#d0e0f0').grid(row=idx, column=0, padx=10, pady=5, sticky=tk.W)
            entry = ttk.Entry(self.root, width=30)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            self.entries[label] = entry
        
        # Botones de operación
        ttk.Button(self.root, text="Agregar", command=self.add_record, style='TButton').grid(row=len(self.labels), column=0, padx=10, pady=5)
        ttk.Button(self.root, text="Mostrar", command=self.show_records, style='TButton').grid(row=len(self.labels), column=1, padx=10, pady=5)
        ttk.Button(self.root, text="Actualizar", command=self.update_record, style='TButton').grid(row=len(self.labels)+1, column=0, padx=10, pady=5)
        ttk.Button(self.root, text="Eliminar", command=self.delete_record, style='TButton').grid(row=len(self.labels)+1, column=1, padx=10, pady=5)
        
        # Listbox para mostrar los registros
        self.records_listbox = tk.Listbox(self.root, width=50, bg='#e0f0f0', borderwidth=2, relief="sunken")
        self.records_listbox.grid(row=0, column=2, rowspan=len(self.labels)+2, padx=10, pady=5)
        
        self.records_listbox.bind('<<ListboxSelect>>', self.load_record)
        
        # Estilo de los botones
        style = ttk.Style()
        style.configure('TButton', background='#add8e6', foreground='black')

    def add_record(self):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO FaunaFlora (ID, NombreCientifico, Habitat, EstadoConservacion, RegionGeografica) VALUES (%s, %s, %s, %s, %s)"
            values = (
                self.entries['ID'].get(),
                self.entries['Nombre Científico'].get(),
                self.entries['Hábitat'].get(),
                self.entries['Estado de Conservación'].get(),
                self.entries['Región Geográfica'].get()
            )
            cursor.execute(query, values)
            self.connection.commit()
            messagebox.showinfo("Éxito", "Registro agregado exitosamente")
        except Error as e:
            messagebox.showerror("Error", f"Error al agregar registro: {e}")
        finally:
            cursor.close()
            self.show_records()
    
    def show_records(self):
        self.records_listbox.delete(0, tk.END)
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM FaunaFlora"
            cursor.execute(query)
            records = cursor.fetchall()
            for record in records:
                self.records_listbox.insert(tk.END, record)
        except Error as e:
            messagebox.showerror("Error", f"Error al mostrar registros: {e}")
        finally:
            cursor.close()
    
    def load_record(self, event):
        try:
            selected_record = self.records_listbox.get(self.records_listbox.curselection())
            for idx, label in enumerate(self.labels):
                self.entries[label].delete(0, tk.END)
                self.entries[label].insert(0, selected_record[idx])
        except IndexError:
            # Manejo del caso en que no se ha seleccionado ningún registro
            pass
    
    def update_record(self):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE FaunaFlora SET NombreCientifico=%s, Habitat=%s, EstadoConservacion=%s, RegionGeografica=%s WHERE ID=%s"
            values = (
                self.entries['Nombre Científico'].get(),
                self.entries['Hábitat'].get(),
                self.entries['Estado de Conservación'].get(),
                self.entries['Región Geográfica'].get(),
                self.entries['ID'].get()
            )
            cursor.execute(query, values)
            self.connection.commit()
            messagebox.showinfo("Éxito", "Registro actualizado exitosamente")
        except Error as e:
            messagebox.showerror("Error", f"Error al actualizar registro: {e}")
        finally:
            cursor.close()
            self.show_records()
    
    def delete_record(self):
        try:
            selected_record = self.records_listbox.get(self.records_listbox.curselection())
            cursor = self.connection.cursor()
            query = "DELETE FROM FaunaFlora WHERE ID=%s"
            cursor.execute(query, (selected_record[0],))
            self.connection.commit()
            messagebox.showinfo("Éxito", "Registro eliminado exitosamente")
        except Error as e:
            messagebox.showerror("Error", f"Error al eliminar registro: {e}")
        finally:
            cursor.close()
            self.show_records()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaunaFloraApp(root)
    root.protocol("WM_DELETE_WINDOW", app.connection.close)  # Cierra la conexión al cerrar la ventana
    root.mainloop()
