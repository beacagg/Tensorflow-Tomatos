# -*- coding: utf-8 -*-

# deep convolution neural networks to detect tomato diseases

# import imutils
from imutils.video import VideoStream
import cv2
import Tkinter as tk
from PIL import Image
from PIL import ImageTk
import threading
import datetime
import time
import os
# import sys
import tensorflow as tf

stopEvent = threading.Event()
pause_ = False
stop_ = False
outputPath = "/home/beatriz/PycharmProjects/Tensorflow-Tomatos"  # alterar para o path correto do projeto
root = tk.Tk()
root.overrideredirect(True)
root.geometry("{0} x {1} + 0 + 0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
print root.winfo_screenwidth(), root.winfo_screenheight()

video = VideoStream(usePiCamera=True, resolution=(640, 480)).start()
video.set(3, 1024)
video.set(4, 720)
time.sleep(0.2)


def videoLoop():
    global panel
    global frame
    while not stop_:
        try:
            while not stopEvent.is_set() and not stop_:
                frame = video.read()
                """
                 O OpenCV representa imagens na ordem BGR (blue, green, red), contudo
                 o PIL representa imagens na ordem RGB, então precisamos trocar os canais
                 e reverter para o formato PIL e ImageTK
                """
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = image.resize((320, 240), Image.ANTIALIAS)
                image = ImageTk.PhotoImage(image)

                # se o painel for none devemos inicia-lo
                if panel is None:
                    panel = tk.Label(image=image)
                    panel.image = image
                    panel.grid(row=1, colunm=2, colunmspan=2, rowspan=3, sticky=tk.W + tk.E + tk.N + tk.S)
                else:
                    panel.configure(image=image)
                    panel.image = image
            while pause_ and not stop_:
                if panel is None:
                    panel = tk.Label(image=image)
                    panel.image = image
                    panel.grid(row=1, colunm=2, colunmspan=2, rowspan=3, sticky=tk.W + tk.E + tk.N + tk.S)
                else:
                    panel.configure(image=image)
                    panel.image = image
        except RuntimeError, e:
            pass


# funcao para detectar e classificar as folhas de tomate
def folhasTomate():
    # timestamp atual para constuir caminho de saida
    ts = datetime.datetime.now()
    # nome do arquivo formatado em jpg, data e hora
    filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
    p = os.path.sep.join((outputPath, filename))

    # salvar o arquivo
    cv2.imwrite(p, frame.copy())
    txt.delete(1.0, tk.END)
    txt.insert(tk.END, "[INFO] salvo {}".format(filename) + "\n")

    # reconhecimento da imagem
    image_path = filename
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()
    # classificacao da imagem com as labels geradas no treinamento do tomate_retrain.py
    label_lines = [line.rstrip() for line in
                   tf.gfile.GFile("tf_files/retrained_labels.txt")]  # tem que corresponder ao path do projeto

    # grafico
    with tf.gfile.FastGFile("tf_files/retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # alimentar o image_data como uma entrada para o grafico
        # softmax tensor - camada softmax: camada de classificacao da rede
        softmax_tensor = sess.graph_def.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            txt.insert(tk.END, '%s (score = %.5f)' % (human_string, score) + "\n")


def stop():
    # evento de parada, limpar camera
    # o processo de saida
    global stop_
    stop_ = True
    print("[INFO] fechando ...")
    stopEvent.set()
    video.stop()
    root.quit()
    root.destroy()
    os._exit()


def play():
    global pause_
    stopEvent.clear()
    pause_ = False
    btn3.grid_remove()
    btn1.grid()
    txt.delete(1.0, tk.END)
    txt.insert(tk.END,
               "Bem vindo(a)\nao Tomato Diseases\n\n\n Por favor, \ncoloque uma imagem no\nsensor \ne clique em INICIAR.\n")


def pause():
    global pause_
    pause_ = True
    stopEvent.set()
    btn1.grid_remove()
    btn3.grid()


def multifunction(*args):
    for function in args:
        function()


# Construindo a interface pelo Tkinter e chamando as funcoes pelos botoes

frame = None
thread = None
panel = None

# botoes das funcoes start/stop/pause
btn1 = tk.Button(root, text="Iniciar", command=lambda: multifunction(folhasTomate, pause), height=2, width=7)
btn2 = tk.Button(root, text="Sair", command=stop, height=2, width=7)
btn3 = tk.Button(root, text="Continuar", command=play, height=2, width=7)

# grids dos botoes
btn1.grid(row=1, colunm=0, rowspan=1, colunmspan=1, sticky=tk.W + tk.E + tk.N + tk.S)
btn2.grid(row=4, colunm=0, rowspan=1, colunmspan=1, sticky=tk.W + tk.E + tk.N + tk.S)
btn3.grid(row=1, colunm=0, rowspan=1, colunmspan=1, sticky=tk.W + tk.E + tk.N + tk.S)
btn3.grid_remove()

txt = tk.Text(root, height=20, width=30)
txt.grid(row=1, colunm=7, rowspan=6, colunmspan=4, sticky=tk.W + tk.E + tk.N + tk.S)
txt.insert(tk.END,
           "Bem vindo(a)\nao Tomato Diseases\n\n\n Por favor, \ncoloque uma imagem no\nsensor \ne clique em INICIAR.\n")

# video stream
thread = threading.Thread(target=videoLoop, args=())
thread.start()

root.wm_title("Tomato Diseases")
root.mainloop()
