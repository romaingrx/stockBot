StockBot
=====

How to run scripts
----

- You need to create and activate a virtual environment

    ```python
    $ python -m venv StockBot
    $ source StockBot/bin/activate
    ```

- And you need to install librairies from requirements.txt

    ```python
    $ pip install pip --upgrade
    $ pip install -r requirements.txt
    ```

Then you are able to execute scripts that are in the examples folder

TensorBoard
----
- To launch the TensorBoard, execute the command below and follow instructions
    ```python
        $ tensorboard --logdir res/tensorboards/
    ```


Examples
----
#####1. naive_LSTM

naive_LSTM is a simple neural network with only one LSTM layer.
