import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

fig, ax = plt.subplots()

line1, = ax.plot(x, y1, label='Seno', color='blue')
line2, = ax.plot(x, y2, label='Coseno', color='orange')

ax.set_xlabel('Eje X (Tiempo)')
ax.set_ylabel('Eje Y (Amplitud)')
ax.set_title('Gráfico interactivo: Seno y Coseno')

ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
ax.legend(loc='upper right')

annot = ax.annotate( #ax.annotate crea un cuadro de texto que mostrara los valores
    "", xy=(0, 0), xytext=(10, 10), #xy: coordenadas iniciales (se actualizan dinamicamente) xytext:offset del texto respecto al cursor
    textcoords="offset points", #Define como se posiciona el texto
    bbox=dict(boxstyle="round", fc="w"), #Estilo del cuadro (redondeado y blanco)
    arrowprops=dict(arrowstyle="->") #Estilo de flecha apuntando al punto
)
annot.set_visible(False)

#Función para actualizar el anotador
def update_annot(line,ind):
    x_val, y_val = line.get_data() #Obtiene los datos (x,y) de la linea
    annot.xy = (x_val[ind['ind'][0]], y_val[ind['ind'][0]]) #Posiciona el anotador en las coordenadas del punto actual.
    text = f'x: {x_val[ind['ind'][0]]:.2f}\ny: {y_val[ind['ind'][0]]:.2f}'
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor(line.get_color()) #Cambia el color del cuadro al color de la linea.
    annot.get_bbox_patch().set_alpha(0.8) #Ajusta transparencia del cuadro

#Función para manejar el movimiento del mouse
def on_move(event): #event: información del evento del cursor.
    visible = annot.get_visible()
    for line in [line1, line2]:
        cont, ind = line.contains(event) #Verifica si el cursor esta sobre la linea
        if cont:
            update_annot(line, ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
            return
        if visible:
            annot.set_visible(False)
            fig.canvas.draw_idle()

#mpl_connect conecta el evento motion_notify_event (movimiento del mouse) a la funcion on_move
fig.canvas.mpl_connect('motion_notify_event',on_move)

plt.show()

