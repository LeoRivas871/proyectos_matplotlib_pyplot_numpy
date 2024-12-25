from pathlib import Path
import csv
import matplotlib.pyplot as plt
from datetime import datetime


path = Path('3881812.csv')
def obtener_datos(path):
    route = Path(path)
    lines = route.read_text().splitlines()
    reader = csv.reader(lines)
    header_row = next(reader)

    #Fechas y temperaturas maximas
    dates, highs, lows = [], [], []
    for row in reader:
        current_date = datetime.strptime(row[2],'%Y-%m-%d')
        high = float(row[7])
        low = float(row[8])
        dates.append(current_date)
        highs.append(high)
        lows.append(low)

    return dates, highs, lows

dates, highs, lows = obtener_datos(path)


plt.plot(dates, highs,label='Maximas', color='red')
plt.plot(dates, lows,label='Minimas', color='blue')
plt.fill_between(dates, highs, lows, facecolor='blue',alpha=0.2)

plt.title('Temperaturas maximas y minimas de New York 2024')
plt.xlabel('Fechas')
plt.ylabel('Max y Min')
plt.grid(color='gray',linestyle='--',linewidth=0.5,alpha=0.7)
plt.legend(loc='upper right')

plt.show()