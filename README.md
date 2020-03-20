StockBot
=====
<p align="center">
<img src="https://bullishbears.com/wp-content/uploads/2018/07/AI-TRADING-1.png">
</p>

How to run scripts
----

- You need to create and activate a virtual environment

    ```shell
    $ python -m venv StockBot
    $ source StockBot/bin/activate
    ```

- And you need to install librairies from requirements.txt

    ```shell
    $ pip install pip --upgrade
    $ pip install -r requirements.txt
    ```

Then you are able to execute scripts that are in the examples folder

TensorBoard
----
- To launch the TensorBoard, execute the command below and follow instructions
    ```shell
    $ tensorboard --logdir res/tensorboards/
    ```


Examples
----
#### naive_LSTM

naive_LSTM is a simple neural network with only one LSTM layer.
