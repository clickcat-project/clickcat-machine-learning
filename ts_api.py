import json
import sys
from flask import Flask, request
import joblib
import pandas as pd
from clickhouse_driver import Client

from sklearn.ensemble import RandomForestRegressor

from skforecast.ForecasterAutoreg import ForecasterAutoreg
from skforecast.model_selection import backtesting_forecaster

app = Flask(__name__)


@app.route('/list', methods=['POST'])
def list():
    json_param = request.json
    conn_host = json_param['conn_host']
    conn_database = json_param['conn_database']
    conn_user = json_param['conn_user']
    conn_password = json_param['conn_password']
    client = Client(conn_host, '9000', conn_database, conn_user, conn_password)
    client.execute('''CREATE DATABASE IF NOT EXISTS clickcat;''')
    client.execute('''CREATE TABLE IF NOT EXISTS clickcat.ML_TASK
                        ( ID             String     NOT NULL,
                          JOB_DETAIL     String    NOT NULL
                        ) ENGINE  = MergeTree ORDER BY ID;
                   ''')
    list = client.execute('select * from clickcat.ML_TASK')
    return json.dumps(list)

@app.route('/train', methods=['POST'])
def train():
    json_param = request.json
    database = json_param['database']
    table = json_param['table']
    time_field = json_param['time_field']
    start_time = json_param['start_time']
    end_time = json_param['end_time']
    job_name = json_param['job_name']
    conn_host = json_param['conn_host']
    conn_database = json_param['conn_database']
    conn_user = json_param['conn_user']
    conn_password = json_param['conn_password']
    client = Client(conn_host, '9000', conn_database, conn_user, conn_password)
    client.execute('''CREATE DATABASE IF NOT EXISTS clickcat;''')
    client.execute('''CREATE TABLE IF NOT EXISTS clickcat.ML_TASK
                        ( ID             String     NOT NULL,
                          JOB_DETAIL     String    NOT NULL
                        ) ENGINE  = MergeTree ORDER BY ID;
                   ''')

    sql = "select toDate(" + time_field + ") as date,count() as count from " + database + "." + table + " where " + time_field + " >=  '" + start_time + "' and " + time_field + " <= '" + end_time + "'  group by toDate(" + time_field + ")"
    list = client.execute(sql)
    print(sql)
    data = pd.DataFrame(list, columns=['date', 'count'])
    data = data.set_index('date')
    data = data.sort_index()
    data.head()
    forecaster = ForecasterAutoreg(
        regressor=RandomForestRegressor(random_state=123),
        lags=6
    )
    forecaster.fit(y=data['count'])
    model_path = f'model/' + job_name + '_ts_model.pkl'
    joblib.dump(forecaster, model_path)
    json_param['model_path'] = model_path
    client.execute(
        "INSERT INTO clickcat.ML_TASK (ID,JOB_DETAIL) VALUES (generateUUIDv4(),'"+json.dumps(json_param)+"')");
    return json_param


@app.route('/back_testing', methods=['POST'])
def back_testing():
    json_param = request.json
    database = json_param['database']
    table = json_param['table']
    time_field = json_param['time_field']
    start_time = json_param['start_time']
    end_time = json_param['end_time']
    conn_host = json_param['conn_host']
    conn_database = json_param['conn_database']
    conn_user = json_param['conn_user']
    conn_password = json_param['conn_password']
    model_path = json_param['model_path']
    client = Client(conn_host, '9000', conn_database, conn_user, conn_password)
    client.execute("set max_bytes_before_external_group_by=100000000000")
    client.execute("set max_memory_usage=200000000000")
    sql = "select toDate(" + time_field + ") as date,count() as count from " + database + "." + table + " where " + time_field + " >=  '" + start_time + "' and " + time_field + " <= '" + end_time + "'  group by toDate(" + time_field + ")"
    list = client.execute(sql)
    print(sql)
    data = pd.DataFrame(list, columns=['date', 'count'])
    data = data.set_index('date')
    data = data.sort_index()
    data.head()

    forecaster = joblib.load(model_path)
    steps = 1
    metric, predictions_backtest = backtesting_forecaster(
        forecaster=forecaster,
        y=data['count'],
        initial_train_size=6,
        fixed_train_size=False,
        steps=steps,
        metric='mean_squared_error',
        refit=True,
        verbose=True
    )
    return pd.DataFrame([data, predictions_backtest]).to_json()


@app.route('/predict', methods=['POST'])
def predict():
    json_param = request.json
    model_path = json_param['model_path']
    steps = json_param['steps']
    forecaster = joblib.load(model_path)
    predictions = forecaster.predict(steps)
    predictions.head(steps)
    return predictions.to_json()


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except Exception as e:
        port = 8080
    app.run(host='0.0.0.0', port=port, debug=False)
