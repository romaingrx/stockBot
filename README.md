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

- Now you need to install librairies from requirements.txt
    ```shell
    $ pip install pip --upgrade
    $ pip install -r requirements.txt
    ```

- To fetch data from online sources, you need to get your API Key from [Quandl](https://www.quandl.com/) and [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
    - So, create an account and get both keys.
    - Then you can launch the command below
    ```shell
        python stockBot --config --alphavantage={YOUR ALPHAVANTAGE KEY} --quandl=
        {YOUR QUANDL KEY}
    ```
    - If everything went well, you can restart your terminal and you're done.
    - After restarting your terminal, you can check if the keys are set with:
    ```shell
        python --config --check
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
