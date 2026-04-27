import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re
 
DATA_FILE = "data.json"
 
class TrainingPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("900x600")
 
        self.trainings = self.load_data()
        self.displayed_trainings = self.trainings.copy()
 
        filter_frame = ttk.LabelFrame(root, text="Фильтр", padding="5")
        filter_frame.pack(fill="x", padx=10, pady=5)
 
        ttk.Label(filter_frame, text="Тип:").pack(side="left", padx=5)
        self.filter_type_var = tk.StringVar(value="Все")
        type_options = ["Все", "Кардио", "Силовая", "Растяжка", "Йога"]
        self.filter_type_combobox = ttk.Combobox(filter_frame, textvariable=self.filter_type_var, values=type_options, state="readonly", width=12)
        self.filter_type_combobox.pack(side="left", padx=5)
 
        ttk.Label(filter_frame, text="Дата (ДД.ММ.ГГГГ):").pack(side="left", padx=5)
        self.filter_date_entry = ttk.Entry(filter_frame, width=12)
        self.filter_date_entry.pack(side="left", padx=5)
 
        ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter).pack(side="left", padx=5)
 
        input_frame = ttk.LabelFrame(root, text="Добавить тренировку", padding="10")
        input_frame.pack(fill="x", padx=10, pady=5)
 
        ttk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky="w", pady=2)
        self.date_entry = ttk.Entry(input_frame, width=20)
        self.date_entry.grid(row=0, column=1, sticky="we", pady=2)
 
        ttk.Label(input_frame, text="Тип:").grid(row=1, column=0, sticky="w", pady=2)
        self.type_var = tk.StringVar()
        type_values = ["Кардио", "Силовая", "Растяжка", "Йога"]
        self.type_combobox = ttk.Combobox(input_frame, textvariable=self.type_var, values=type_values, state="readonly", width=17)
        self.type_combobox.grid(row=1, column=1, sticky="we", pady=2)
        self.type_combobox.current(0)
 
        ttk.Label(input_frame, text="Длительность (мин):").grid(row=2, column=0, sticky="w", pady=2)
        self.duration_entry = ttk.Entry(input_frame, width=20)
        self.duration_entry.grid(row=2, column=1, sticky="we", pady=2)
 
        ttk.Button(input_frame, text="Добавить тренировку", command=self.add_training).grid(row=3, column=0, columnspan=2, pady=10)
 
        btn_frame = ttk.Frame(root)
        btn_frame.pack(fill="x", padx=10, pady=5)
 
        ttk.Button(btn_frame, text="Сбросить фильтр / Показать все", command=self.reset_filter).pack(side="left")
 
        table_container = ttk.Frame(root)
        table_container.pack(fill='both', expand=True, padx=10, pady=5)
 
        yscrollbar = ttk.Scrollbar(table_container, orient="vertical")
        xscrollbar = ttk.Scrollbar(table_container, orient="horizontal")
        
        self.tree = ttk.Treeview(table_container, columns=("date", "type", "duration"), show='headings', yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)
        
        yscrollbar.config(command=self.tree.yview)
        xscrollbar.config(command=self.tree.xview)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        yscrollbar.grid(row=0, column=1, sticky='ns')
        xscrollbar.grid(row=1, column=0, sticky='ew')
         
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
 
    def add_training(self):
         date = self.date_entry.get().strip()
         
         try:
             duration_str = self.duration_entry.get().strip()
             if not duration_str:
                 raise ValueError("Длительность не может быть пустой.")
             duration = int(duration_str)
             if duration <= 0:
                 raise ValueError("Длительность должна быть больше нуля.")
                 
             tr_type = self.type_var.get()
             if not tr_type:
                 raise ValueError("Выберите тип тренировки.")
                 
             if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", date):
                 raise ValueError("Неверный формат даты. Используйте ДД.ММ.ГГГГ.")
                 
             self.trainings.append({"date": date, "type": tr_type, "duration": duration})
             self.displayed_trainings = self.trainings.copy()
             self.update_treeview()
             
             self.date_entry.delete(0, tk.END)
             self.duration_entry.delete(0, tk.END)
             self.save_data()
             
             messagebox.showinfo("Успех", "Тренировка добавлена!")
             
         except ValueError as e:
             messagebox.showerror("Ошибка ввода", str(e))
 
    def update_treeview(self):
         for i in self.tree.get_children():
             self.tree.delete(i)
         
         for training in self.displayed_trainings:
             self.tree.insert("", tk.END, values=(training["date"], training["type"], training["duration"]))
 
    def apply_filter(self):
         filter_type = self.filter_type_var.get()
         filter_date = self.filter_date_entry.get().strip()
         
         filtered_list = []
         
         for item in self.trainings:
             type_match = (filter_type == "Все") or (item["type"] == filter_type)
             date_match = (filter_date == "") or (item["date"] == filter_date)
             
             if type_match and date_match:
                 filtered_list.append(item)
                 
         self.displayed_trainings = filtered_list
         self.update_treeview()

    def reset_filter(self):
         self.filter_type_var.set("Все")
         self.filter_date_entry.delete(0, tk.END)
         self.displayed_trainings = self.trainings.copy()
         self.update_treeview()
 
    def save_data(self):
          try:
              with open(DATA_FILE, 'w', encoding='utf-8') as f:
                  json.dump(self.trainings, f, ensure_ascii=False, indent=4)
          except Exception as e:
              messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить данные: {e}")
 
    def load_data(self):
          if os.path.exists(DATA_FILE):
              try:
                  with open(DATA_FILE, 'r', encoding='utf-8') as f:
                      return json.load(f)
              except Exception as e:
                  messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить данные: {e}")
                  return []
          return []
 
if __name__ == "__main__":
     root = tk.Tk()
     app = TrainingPlannerApp(root)
     root.mainloop()
