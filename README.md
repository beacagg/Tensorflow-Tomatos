# Tomato Diseases

CNNs, Deep Learning e Transfer learning para classificação de folhas de tomate com doenças.

## Getting Started

### Pré-requisitos
* Python 3
* Tensorflow
* Tensorboard
* Numpy
* Matplotlib


### Treinamento

#### Atenção: precisa do dataset para funcionar.

Inicialize o Tensorboard para verificar os gráficos de treinamento.

```
tensorboard --logdir=tf_files/retrain_logs
```

Rode o train.sh para retreinar a rede.

```
bash train.sh
```

Se quiser alterar os parametros de treinamento com vi/nano/gedit 
```
vi train.sh
```

OBS: Para ver os gráficos do tensorboard: 

```
localhost:6006
```


## Running 

Para classificar qualquer arquivo que quiser, da sua coleção ou uma nova:	

```
python3 label_image.py \
 --image=tf_files/tomato_early_blight.jpeg  \
 --graph=tf_files/retrained_graph.pb \
 --labels=tf_files/retrained_labels.txt \
 --input_layer=Mul \
 --output_layer=final_result

```


## Authors

* **Beatriz Caggiano** - *Initial work* - [beacagg](https://github.com/beacagg)


## License

This project is licensed under the APACHE License - see the [LICENSE.md](LICENSE.md) file for details

### Obs:
Para rodar o modelo pré-treinado é necessário os valores de bottlenecks. 
https://goo.gl/2QE9Jk <- mais informaçoes.
