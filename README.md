After running 10 epochs (using the EfficientNet-B0 model) incrementally, epoch 8 was discovered to be the best model.

Epoch 1
-------

Training Loss:  0.4481

Training Accuracy: 81.40%

Validation Loss:  0.2642

Validation Accuracy: 89.04%

Epoch 2
-------

Training Loss:  0.2699

Training Accuracy: 88.71%

Validation Loss:  0.2288

Validation Accuracy: 90.81%

Epoch 3
-------

Training Loss:  0.2021

Training Accuracy: 92.67%

Validation Loss:  0.1664

Validation Accuracy: 92.74%

Epoch 4
-------

Training Loss:  0.1478

Training Accuracy: 94.56%

Validation Loss:  0.1451

Validation Accuracy: 93.56%

Epoch 5
-------

Training Loss:  0.1130

Training Accuracy: 96.11%

Validation Loss:  0.1706

Validation Accuracy: 93.33%

Epoch 6
-------

Training Loss:  0.0961

Training Accuracy: 96.57%

Validation Loss:  0.1556

Validation Accuracy: 94.30%

Epoch 7
-------

Training Loss:  0.0752

Training Accuracy: 97.30%

Validation Loss:  0.1842

Validation Accuracy: 93.85%

Epoch 8
-------

Training Loss:  0.0743

Training Accuracy: 97.40%

Validation Loss:  0.1250

Validation Accuracy: 95.85%

Epoch 9
-------

Training Loss:  0.0545

Training Accuracy: 98.02%

Validation Loss:  0.1905

Validation Accuracy: 94.30%

Epoch 10
--------

Training Loss:  0.0591

Training Accuracy: 98.06%

Validation Loss:  0.1716

Validation Accuracy: 94.07%

After Epoch 8, subsequent epochs showed signs of overfitting.

The selected model was run on a new testing dataset of 1350 unseen images and correctly classified 1297/1350 of the images, an accuracy of 96.07%

That gives our model the following stats:
Training accuracy - 97.40%
Validation accuracy - 95.85%
Test accuracy - 96.07%

The Classification report revealed the following:
Confusion Matrix:

  Predicted
  ---------
[425  25   0]
[ 27 423   0]  Actual
[  1   0 449]  ------

          precision  recall   f1-score    support
real       93.82%    94.44%    94.13%       450
synthetic  94.42%    94.00%    94.21%       450
swapped    100.00%   99.78%    99.89%       450

The confusion matrix showed that the model's errors were concentrated almost entirely in the distinction between real and synthetic images, accounting for 52 of the 53 misclassifications. 

The face-swapped class achieved a recall of 99.78% and F1-score of 99.89%, showing that the model learned highly discriminative features for detecting face-swapped content.

Hence the final metrics for the model are as follows:

EfficientNet-B0 — Epoch 8
Metric	            Result
Training accuracy	97.40%
Validation accuracy	95.85%
Test accuracy	    96.07%
Test images	        1,350
Correct	            1,297
Incorrect	        53
Real F1	            94.13%
Synthetic F1	    94.21%
Swapped F1	        99.89%