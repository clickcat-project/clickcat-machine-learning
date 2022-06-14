
1. ### Install PIP requirements
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
         "job_name":"hb_kako_vehicle_recognition_predict",
         "conn_host":"192.168.3.243",
         "conn_database":"default",
         "conn_user":"default",
         "conn_password":"123456"
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
