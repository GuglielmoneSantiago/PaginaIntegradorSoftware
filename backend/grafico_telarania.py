import matplotlib.pyplot as plt
import numpy as np

def generar_grafico_telarana(datos, guardar=False, nombre_archivo='grafico_telarana.png'):
    categorias = list(datos.keys())
    valores = list(datos.values())

    # Añadir el primer valor al final para cerrar el círculo
    valores += valores[:1]

    # Calcular el ángulo de cada eje
    num_categorias = len(categorias)
    angulos = np.linspace(0, 2 * np.pi, num_categorias, endpoint=False).tolist()
    angulos += angulos[:1]  # Añadir el primer ángulo al final para cerrar el círculo

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angulos, valores, 'b', alpha=0.1)

    # Añadir líneas para cada categoría
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(angulos[:-1], categorias)

    # Añadir valores en los ejes
    for i, valor in enumerate(valores):
        ax.text(angulos[i], valor + 0.5, str(valor))

    if guardar:
        fig.savefig(nombre_archivo)
        plt.close(fig)  # Cerrar la figura para liberar memoria
        return nombre_archivo
    else:
        return fig


