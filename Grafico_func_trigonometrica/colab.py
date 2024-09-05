#!apt-get install -y ffmpeg
#!pip install pillow

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from IPython.display import Image, clear_output, display

#####################################
# b_0  Amplitude
# b_1  Frequencia
# b_2  Fase
# b_3  Deslocamento Vertical
#####################################
# Docs :
# FuncAnimation :      https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html
# subplots :           https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html
# Ultima alteração :   02-09-2024
# Repo :               https://github.com/chEfInHO0/Projetos-Faculdade/tree/main/Grafico_func_trigonometrica
#####################################

global animation_frame, x_signal      # Apenas para formatação de saida

###############################################################################
###############################################################################
###     PARA ALTERAR A ANIMAÇÃO, MUDE O VALOR DAS CONSTANTES ABAIXO:        ###
###                 MAX_FRAMES,INTERVAL,FRAME_DIV                           ###
###############################################################################
###############################################################################

# Constantes da animação
MIN_FRAMES = 1          # Minimo 1, deve ser menor que MAX_FRAMES
MAX_FRAMES = 150        # Quanto maior, mais tempo a animação
INTERVAL = 25           # intervalo de atualização de um frame a outro (Recomendado: Max 50)
FRAME_DIV = 10          # FRAME_DIV deve ser superior a 0, diminui a velocidade da animação que usa o frame para mudar o valor (Melhor performance)
AUX_DIV = 5             # No caso da tangente o gráfico pode ficar bem inviável para a visualização então vamos adicionar uma variavel extra para controle


PI,SEN,COS,TG = np.pi, np.sin, np.cos, np.tan # declarando as constantes trigonométricas


SLICES = 5000           # Não aumentar

FIG_X_SIZE = 10         # tamanho do gráfico plotado
FIG_Y_SIZE = 5          # tamanho do gráfico plotado

MIN_LINSPACE = -4 * PI # Inicio do domínio
MAX_LINSPACE = 4 * PI  # Final do domínio

MIN_X_LIM = -4 * PI     # Inicio do grafico do eixo X
MAX_X_LIM = 4 * PI      # Final do grafico do eixo X

MIN_Y_LIM = -40         # Inicio do grafico do eixo Y
MAX_Y_LIM = 40         # Final do grafico do eixo Y

def ask_input(msg: str, input_msg: str, error_msg: str, input_range: list, mult_choice=False):
    """
    Solicita a entrada do usuário com validação de intervalo.

    Args:
        msg (str): Mensagem a ser exibida antes da solicitação.
        input_msg (str): Mensagem solicitando a entrada do usuário.
        error_msg (str): Mensagem exibida quando a entrada não está no intervalo.
        input_range (list): Lista com o intervalo de valores permitidos.

    Returns:
        int: Valor inteiro válido dentro do intervalo especificado.
    """
    print(msg)
    actions = list()
    while True:
        try:
            opt = int(input(input_msg) or -1)
            if opt == (input_range[0]-1):
                print('Saindo...')
                raise SystemExit
            else:
                if opt == -1:
                    return actions if mult_choice else opt
                if opt in input_range:
                    if mult_choice:
                        actions.append(opt) if (
                            opt != -1) and (opt not in actions) else ''
                    else:
                        return opt
                else:
                    print(error_msg)
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

def chart_config():
    # Configuração inicial do gráfico
    fig, ax = plt.subplots(figsize=(FIG_X_SIZE, FIG_Y_SIZE))
    x = np.linspace(MIN_LINSPACE, MAX_LINSPACE, SLICES)  # Domínio
    print(x)
    # Criação da linha inicial no gráfico
    line, = ax.plot(x, SEN(x))

    # Configuração dos limites do gráfico
    ax.set_xlim(MIN_X_LIM, MAX_X_LIM)
    ax.set_ylim(MIN_Y_LIM, MAX_Y_LIM)

    ax.spines['left'].set_position('zero')  # Eixo y sobre o 0 do eixo x
    ax.spines['bottom'].set_position('zero')  # Eixo x sobre o 0 do eixo y

    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    return line,fig,x

def label_chart(chart_name: str, opt: list):
    """
    Essa função gera titulo que fica no gráfico
    chart_name : Seno,Cosseno ou Tangente
    opt:
    """
    labels = ["Amplitude(b_0) variando",
              "Frequência(b_1) variando" if chart_name != 'Tg' else f"Frequência(b_1) variando (velocidade reduzida em {AUX_DIV}x)" ,
              "Fase(b_2) variando",
              "Deslocamento(b_3) vertical alterando"]
    label_selected = f'{chart_name}: '
    for action in opt:
        label_selected += f'{labels[action-1]}, '
    return label_selected

def plot_sin_dynamic(opt, animation_type):
    """
    Plota um gráfico dinâmico do seno, permitindo alterar amplitude, frequência, fase e deslocamento vertical.
    """

    # Função de atualização para animação
    def update(frame):
        global animation_frame, x_signal
        animation_frame = frame
        possible_frame = {
            0: -1*(frame / FRAME_DIV),
            1: (frame / FRAME_DIV)}
        animation_step = possible_frame[animation_type]
        # print(animation_step) evita flood de dados no output do colab
        x_signal = 'positivo' if animation_type > 0 else 'negativo'
        b_0 = animation_step if 1 in opt else 1
        b_1 = animation_step if 2 in opt else 1
        b_2 = animation_step if 3 in opt else 1
        b_3 = animation_step if 4 in opt else 0
        y = (b_0 * SEN((b_1 * x) + b_2)) + b_3  # SENO  a * sen((b*x)*c)+d
        line.set_ydata(y)
        return line,

    line,fig,x = chart_config()

    # Criação da animação
    ani = FuncAnimation(fig, update, frames=np.arange(
        MIN_FRAMES, MAX_FRAMES), interval=INTERVAL, blit=True)
    label_selected = label_chart('Sen', opt)
    plt.title(f'{label_selected} {x_signal}')
    ani.save('animation.gif', writer=PillowWriter(fps=20))
    display(Image(filename='animation.gif'))
    plt.close(fig)


def plot_cos_dynamic(opt, animation_type):
    """
    Plota um gráfico dinâmico do cosseno, permitindo alterar amplitude, frequência, fase e deslocamento vertical.
    """
    # Função de atualização para animação
    def update(frame):
        global animation_frame, x_signal
        animation_frame = frame
        possible_frame = {
            0: -1*(frame / FRAME_DIV),
            1: (frame / FRAME_DIV)}
        animation_step = possible_frame[animation_type]
        # print(animation_step) evita flood de dados no output do colab
        x_signal = 'positivo' if animation_type > 0 else 'negativo'
        b_0 = animation_step if 1 in opt else 1
        b_1 = animation_step if 2 in opt else 1
        b_2 = animation_step if 3 in opt else 1
        b_3 = animation_step if 4 in opt else 0
        y = (b_0 * COS((b_1 * x) + b_2)) + b_3  # COSSENO  a * cos((b*x)*c)+d
        line.set_ydata(y)
        return line,

    line,fig,x = chart_config()

    # Criação da animação
    ani = FuncAnimation(fig, update, frames=np.arange(
        MIN_FRAMES, MAX_FRAMES), interval=INTERVAL, blit=True)
    label_selected = label_chart('Cos', opt)
    plt.title(f'{label_selected} {x_signal}')
    ani.save('animation.gif', writer=PillowWriter(fps=20))
    display(Image(filename='animation.gif'))
    plt.close(fig)


def plot_tg_dynamic(opt, animation_type):
    """
    Plota um gráfico dinâmico da tangente, permitindo alterar amplitude, frequência, fase e deslocamento vertical.
    """
    # Função de atualização para animação
    def update(frame):
        global animation_frame, x_signal
        animation_frame = frame
        possible_frame = {
            0: -1*(frame / FRAME_DIV),
            1: (frame / FRAME_DIV)}
        animation_step = possible_frame[animation_type]
        # print(animation_step) evita flood de dados no output do colab
        x_signal = 'positivo' if animation_type > 0 else 'negativo'
        b_0 = animation_step if 1 in opt else 1
        b_1 = animation_step/AUX_DIV if 2 in opt else 1
        b_2 = animation_step if 3 in opt else 1
        b_3 = animation_step if 4 in opt else 0
        y = (b_0 * TG((b_1 * x) + b_2)) + b_3  # TANGENTE  a * tg((b*x)*c)+d
        line.set_ydata(y)
        return line,

    line,fig,x = chart_config()

    # Criação da animação
    ani = FuncAnimation(fig, update, frames=np.arange(
        MIN_FRAMES, MAX_FRAMES), interval=INTERVAL, blit=True)
    label_selected = label_chart('Tg', opt)
    plt.title(f'{label_selected} {x_signal}')
    ani.save('animation.gif', writer=PillowWriter(fps=20))
    display(Image(filename='animation.gif'))
    plt.close(fig)


def select_chart():
    """
    Retorna uma função e valor correspondente ao nome da função trigonometrica
    """
    chart = {
        1: plot_sin_dynamic,
        2: plot_cos_dynamic,
        3: plot_tg_dynamic
    }
    chart_opt = ask_input('Qual gráfico deseja analisar ?',
                         '0 - Sair\n1 - Seno\n2 - Cosseno\n3 - Tangente \n',
                         'Opção Inválida, tente novamente',
                         [1, 2, 3]
                         )
    return [chart[chart_opt], chart_opt]


def all_charts():
    """
    Retorna uma função e valor correspondente ao nome da função trigonometrica
    """
    chart = {
        1: plot_sin_dynamic,
        2: plot_cos_dynamic,
        3: plot_tg_dynamic
    }
    return [chart[1],chart[2],chart[3]]


def main():
    chart_names = ['Sen', 'Cos', 'Tg']
    b_ = ['b_0','b_1','b_2','b_3']
    # selected_chart,chart_opt = select_chart()
    animation_type = ask_input(
        'Valores Positivos ou Negativos?',
        '0 - Negativos\n1 - Positivos\n: ',
        'Opção inválida, tente novamente',
        [0, 1])

    opt = ask_input(
        f'O que deseja analisar ?', # em {chart_names[chart_opt-1]}
        '1 - Amplitude\n2 - Frequencia\n3 - Fase\n4 - Deslocamento Vertical\n\nPRESSIONE ENTER QUANDO TERMINAR DE ESCOLHER AS ANALISES\n\nDigite a opção: ',
        'Opção inválida, tente novamente.',
        [1, 2, 3, 4],
        True
    )
    clear_output()
    # selected_chart(opt, animation_type) executa só 1 animação
    for chart in all_charts():
      chart(opt,animation_type)

if __name__ == "__main__":
    main()