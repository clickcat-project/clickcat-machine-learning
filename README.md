This is backend for ClickCat Machine Learning. 

1. ### Install PIP requirements
    Python3.6+ is necessary.
    ```
    pip install -r requirements.txt
    ```
2. ### Running API

    ```
    python ts_api.py <port>
    ```

3. ### Endpoints
    ### /list (POST)
     ```
     {
         "conn_host":"192.168.3.243",
         "conn_database":"default",
         "conn_user":"default",
         "conn_password":"123456"
     }
     ```
    ### /train (POST)
     ```
     {
         "database":"default",
         "table":"hb_kako_vehicle_recognition",
         "time_field":"shotTime",
         "start_time":"2022-03-01 00:00:00",
         "end_time":"2022-04-01 00:00:00",
         "time_interval":"1 day",
         "job_name":"hb_kako_vehicle_recognition_predict",
         "conn_host":"192.168.3.243",
         "conn_database":"default",
         "conn_user":"default",
         "conn_password":"123456"
    }
    ```
    ### /delete (POST)
    ```
    {
        "job_id":"010defe2-a0d8-4acb-aa13-10d6e2cfbb87",
        "conn_host":"192.168.3.243",
        "conn_database":"default",
        "conn_user":"default",
        "conn_password":"123456",
        "model_path":"model/hb_kako_vehicle_recognition_predict_ts_model.pkl"
    }
    ```
    ### /back_testing (POST)
    ```
    {
        "database":"default",
        "table":"hb_kako_vehicle_recognition",
        "time_field":"shotTime",
        "start_time":"2022-03-01 00:00:00",
        "end_time":"2022-04-01 00:00:00",
        "time_interval":"1 day",
        "job_name":"hb_kako_vehicle_recognition_predict",
        "conn_host":"192.168.3.243",
        "conn_database":"default",
        "conn_user":"default",
        "conn_password":"123456",
        "model_path":"model/hb_kako_vehicle_recognition_predict_ts_model.pkl"
    }
    ```
    ### /predict (POST)
    ```
    {
        "model_path":"model/hb_kako_vehicle_recognition_predict_ts_model.pkl"
        "steps":"1",
    }
    ```
