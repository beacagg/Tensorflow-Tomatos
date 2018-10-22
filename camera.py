
# so funciona no raspberry pi!!!!

import time
import numpy as np

import cv2

#imports da camera do rasp
import picamera
import picamera.array

#combinar quatro imagens na tela para comparacao

"""
|                   |
| |  im1 |  | im2 | |
|                   |
| |  im3 |  | im4 | |
|                   |
"""

def multiple (im1=None, im2=None, im3=None, im4=None):
	height, width = im1.shape
	combined = np.zeros((2 * height, 2 * width, 3), dtype=np.uint8)

	combined[0:height, 0:width, :] = cv2.cvtColor(im1, cv2.COLOR_GRAY2RGB) #transforma rgb para escalas de cinza
	combined[height:, 0:width, :] = cv2.cvtColor(im2, cv2.COLOR_GRAY2RGB)
	combined[0:height, width:, :] = cv2.cvtColor(im3, cv2.COLOR_GRAY2RGB)
	combined[height: , width: , :] = cv2.cvtColor(im4, cv2.COLOR_GRAY2RGB)

	return combined

#adicionar textos nas camadas de imagem fornecidas
def label(image, text):
	#font = cv2.FONT_HERSHEY_SIMPLEX
    	#CV_FONT_HERSHEY_SIMPLEX normal size sans-serif font
	return cv2.putText(image, text, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)

#ajusta o contraste nas imagens, de 5 a 95%
def contraste(im):
	in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)

    # brilho minimo
    out_min = 0.0
    # brilho maximo
    out_max = 255.0

    # a saida sera a diferenca entre os brilhos / a diferenca dos contrastes
    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out

#executando a camera do rasp
def run():
    with picamera.PiCamera() as camera:
        #resolucao da camera
        x = 400
        camera.resolution = (int(1.33 * x), x )

        #tempo de descanso pra a camera se configurar
        time.sleep(1)

        with picamera.array.PiRGBArray(camera) as stream:
            while True:
                # pega os dados de cor e formato da camera
                # IMPORTANTE: a ordem das cores vem em ordem BGR ao inves de RGB (sera importante depois!)
                camera.capture(stream, format='bgr', use_video_port=True)
                image = stream.array

                #pega os componentes da imagem individualmente
                b, g, r = cv2.split(image)

                # calcular o NDVI (Normalized Difference Vegetation Index)

                bottom = (r.astype(float) + b.astype (float))
                bottom[bottom == 0] = 0.01

                ndvi = (r.astype(float) - b) / bottom
                ndvi = contraste(ndvi)
                ndvi = ndvi.astype(np.uint8)

                label(b, 'Blue')
                label(g, 'Green')
                label(r, 'NIR')
                label(ndvi, 'NDVI')

                combined = multiple(b, g, r, ndvi)

                cv2.imshow('image', combined)

                stream.truncate(0)

                # Pressionar ESC para sair do loop
                c = cv2.waitKey(7) % 0x100
                if c == 27:
                    break

        cv2.imwrite('images/r.jpg', r)
        cv2.imwrite('images/g.jpg', g)
        cv2.imwrite('images/b.jpg', b)
        cv2.imwrite('images/ndvi.jpg', ndvi)
        cv2.destroyAllWindows()

if __name__ = '__main__':
    run()








