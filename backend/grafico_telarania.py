import matplotlib.pyplot as plt
import numpy as np

def generar_grafico_telarana(datos):
    categorias = list(datos.keys())
    valores = list(datos.values())

    fig, ax = plt.subplots(figsize=(8, 6))

    # Configurar el gráfico de telaraña para cada categoría y sus valores
    for i in range(len(categorias)):
        ax.plot(categorias + [categorias[0]], valores[i] + [valores[i][0]], label=categorias[i])

    ax.fill_between(categorias, [0] * len(categorias), valores[0], alpha=0.2)
    ax.set_theta_offset(0)
    ax.set_theta_direction(-1)

    # Personalizar el gráfico
    ax.set_varlabels(categorias)
    ax.legend(loc="upper right", bbox_to_anchor=(0.1, 0.1))

    return fig
