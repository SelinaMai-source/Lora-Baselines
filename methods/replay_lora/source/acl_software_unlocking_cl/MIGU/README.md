# Cluster activate lora

## Setup

You can install the required libraries by running 

```
pip install -r requirements.txt
```

You are also required to download the t5-large model from huggingface, put it to the folder named ```initial_model```, and rename the model folder as 't5-large'.

LLaMA2 HF is also supported. You can put your llama2 hf model to the folder named ```initial_model``` and rename the model folder as 'llama'.


## Training and Evaluation

For t5-large:

You can reproduce our experiments of order 1 & 2 & 3 by simply running

order1:

```
/data/chengshuang/CL/cluster-lora-submit/scripts/run_order1.sh
```

order2:

```
/data/chengshuang/CL/cluster-lora-submit/scripts/run_order2.sh
```

order3:

```
/data/chengshuang/CL/cluster-lora-submit/scripts/run_order3.sh
```

The model you have trained will be saved in ```outputs```.
