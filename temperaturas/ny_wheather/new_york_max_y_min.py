from pathlib import Path
import csv
import matplotlib.pyplot as plt
from datetime import datetime

# Ruta al archivo CSV
path = Path('ny_2024.csv')

# Función para obtener datos del CSV
def obtener_datos(path):
    route = Path(path)
    lines = route.read_text().splitlines()
    reader = csv.DictReader(lines)  # Usar DictReader para leer por nombres de columna

    # Fechas y temperaturas máximas y mínimas
    dates, highs, lows = [], [], []
    for row in reader:
        # Acceder a las columnas por su nombre
        current_date = datetime.strptime(row["DATE"], '%Y-%m-%d')
        try:
            high = float(row["TMAX"]) if row["TMAX"] else None
            low = float(row["TMIN"]) if row["TMIN"] else None
        except ValueError:
            continue  # Ignorar filas con valores inválidos

        dates.append(current_date)
        highs.append(high)
        lows.append(low)

    return dates, highs, lows

# Cargar datos
dates, highs, lows = obtener_datos(path)

# Calcular valores para la leyenda
max_temp = max(highs)
min_temp = min(lows)
temp_diff = max_temp - min_temp

# Crear gráfico
fig, ax = plt.subplots()

# Ploteo de las líneas
line1, = ax.plot(dates, highs, label=f'Máximas (Máx: {max_temp}°C)', color='red')
line2, = ax.plot(dates, lows, label=f'Mínimas (Mín: {min_temp}°C)', color='blue')
ax.fill_between(dates, highs, lows, facecolor='blue', alpha=0.2)

# Añadir la diferencia a la leyenda
plt.legend(
    title=f"Diferencia: {temp_diff:.2f}°C", loc='upper right', fontsize=9
)

plt.title('Temperaturas máximas y mínimas de New York 2024')
plt.xlabel('Fechas')
plt.ylabel('Temperaturas')
plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

# Crear el anotador
annot = ax.annotate(
    "", xy=(0, 0), xytext=(10, 10),
    textcoords="offset points",
    bbox=dict(boxstyle="round", fc="w"),
    arrowprops=dict(arrowstyle="->")
)
annot.set_visible(False)

# Función para actualizar el anotador
def update_annot(line, ind):
    x_val, y_val = line.get_data()
    x, y = x_val[ind["ind"][0]], y_val[ind["ind"][0]]
    date = dates[ind["ind"][0]].strftime("%Y-%m-%d")  # Formatea la fecha
    annot.xy = (x, y)
    text = f"Fecha: {date}\nTemperatura: {y:.2f}°C"  # Agrega el símbolo de grados
    annot.set_text(text)
    bbox = annot.get_bbox_patch()
    bbox.set_facecolor(line.get_color())  # Cambia el color de fondo al de la línea
    bbox.set_alpha(0.9)  # Ajusta la transparencia para el sombreado
    bbox.set_edgecolor("black")  # Agrega un borde negro para mayor claridad

# Función para manejar el movimiento del mouse
def on_move(event):
    visible = annot.get_visible()
    for line in [line1, line2]:
        cont, ind = line.contains(event)
        if cont:
            update_annot(line, ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
            return
    if visible:
        annot.set_visible(False)
        fig.canvas.draw_idle()

# Conectar el evento de movimiento del mouse
fig.canvas.mpl_connect('motion_notify_event', on_move)

plt.show()
