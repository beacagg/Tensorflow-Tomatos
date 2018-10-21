python3 label_image.py \
 --image=tf_files/tomato_early_blight.jpeg  \
 --graph=tf_files/retrained_graph.pb \
 --labels=tf_files/retrained_labels.txt \
 --input_layer=Mul \
 --output_layer=final_result
