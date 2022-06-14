import requests
host = "http://localhost:8080"



payload = {
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


r = requests.post(f"{host}/train", json=payload)
print(r.text)



payload = {
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


r = requests.post(f"{host}/back_testing", json=payload)
print(r.text)
