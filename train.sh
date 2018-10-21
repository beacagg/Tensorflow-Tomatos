python3 tomato_retrain.py \
 --output_graph=tf_files/retrained_graph.pb \
 --output_label=tf_files/retrained_labels.txt \
 --image_dir=tf_files/dataset_min \
 --bottleneck_dir=tf_files/bottlenecks \
 --how_many_training_steps=1000 \
 --learning_rate=.03 \
 --train_batch_size=300 \
 --validation_batch_size=200 \
