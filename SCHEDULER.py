import paho.mqtt.client as mqtt
import pandas as pd
from datetime import datetime
from CTkMessagebox import CTkMessagebox
import time, json, uuid, time, customtkinter, csv

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

broker_address = "3.1.133.191"
port = 1895
topic_response = []

sum_res = []

client_id = str(uuid.uuid4())

client = mqtt.Client(client_id=client_id)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("SCHEDULER")
        self.iconbitmap('assets/iconx.ico')
        # self.geometry(f"{1100}x{580}")

        # configure grid layout
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.FR1 = customtkinter.CTkFrame(self, width=0, corner_radius=0, border_width=0)
        self.FR1.grid(row=10, column=2, sticky="nsew")
        self.FR1.grid_rowconfigure(10, weight=1)

        self.btn_load = customtkinter.CTkButton(self.FR1, width=520, text="INPUT LIST", command=load_list)
        self.btn_load.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # self.label = customtkinter.CTkLabel(self.FR1, text="POST SCHEDULE", font=customtkinter.CTkFont(size=15, weight="bold"))
        # self.label.grid(row=0, column=0,  padx=10, pady=10)

        self.post_result = customtkinter.CTkTextbox(self.FR1, width=250, height=400, corner_radius=10)
        self.post_result.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.received_result = customtkinter.CTkTextbox(self.FR1, width=250, height=400, corner_radius=10)
        self.received_result.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.input_time = customtkinter.CTkEntry(self.FR1, width=250, placeholder_text="INPUT TIME")
        self.input_time.grid(row=2, column=0, padx=10, pady=10)

        self.save_btn = customtkinter.CTkButton(self.FR1, width=250, text="SAVE LOG", command=save_log)
        self.save_btn.grid(row=2, column=1, padx=10, pady=10)
        
        self.execute_btn = customtkinter.CTkButton(self.FR1, width=250, text="EXECUTE", command=execute)
        self.execute_btn.grid(row=3, column=0, padx=10, pady=10)

        self.clear_btn = customtkinter.CTkButton(self.FR1, width=250, text="CLEAR", command=clear_text_box)
        self.clear_btn.grid(row=3, column=1, padx=10, pady=10)

        self.label = customtkinter.CTkLabel(self.FR1, text="mahesa.gilang@efishery.com", font=customtkinter.CTkFont(size=10))
        self.label.grid(row=4, column=0, columnspan=2, padx=0, pady=0, sticky="nsew")

def clear_text_box():
    app.post_result.delete(0.0,"end")
    app.received_result.delete(0.0,"end")
    sum_res.clear()

def save_log():
    post = app.post_result.get("1.0", "end-1c")
    res  = app.received_result.get("1.0", "end-1c")
    if post and res:
        with open("dummy.txt", 'a') as file:
            file.write(f"{post}\n")
            file.write(f"RESULT :\n")
            file.write(f"{res}\n")
            file.write(f"*************************************\n")
            file.write(f"\n")
    else:
        CTkMessagebox(title="Message",width=150,height=100,message="Log is empty",icon="assets/icon.png",option_1="ok")

def load_list():
    global df,row,file_path
    try:
        client.loop_stop()
        client.disconnect()
        topic_response.clear()
        file_path = customtkinter.filedialog.askopenfilename(title="Select a csv file")
        print(file_path)
        app.btn_load.configure(text=file_path)
        csvdata = pd.read_csv(str(file_path))
        df = pd.DataFrame(csvdata)
        row = len(df.index)

        for i in range(0, row):
            UUID = df.at[df.index[i],'UUID']
            dummy = f"aiot/iot-device/{UUID}/command/response"
            topic_response.append(dummy)
        client.connect(broker_address, port, 60)
        client.loop_start()
    except Exception as e:
        CTkMessagebox(title="Message",width=150,height=100,message="Wrong input",icon="assets/icon.png",option_1="ok")
        return "false"

def time_set():
    try:
        time_string = app.input_time.get()
        time_values = time_string.split(".")
        hours = int(time_values[0])
        # print(hours)
        if 7 > hours >= 0:
            jam = (int(time_values[0]) + 17) * 3600
            menit = int(time_values[1]) * 60
            schedule_time = jam + menit
            # print("minus",(jam+menit))
            return schedule_time
        if 23 >= hours >= 7 :
            jam = (int(time_values[0]) - 7) * 3600
            menit = int(time_values[1]) * 60
            schedule_time = jam + menit
            # print("plus",(jam+menit))
            return schedule_time
        return schedule_time
    except Exception as e:
        CTkMessagebox(title="Message",width=150,height=100,message="Please input time correcttly",icon="assets/icon.png",option_1="ok")
        return "false"

def execute():
    try:
        schedule_time = time_set()
        time_post = datetime.fromtimestamp(schedule_time).strftime("%H:%M:%S")
        current_epoch_time = int(time.time())

        converted_datetime = datetime.fromtimestamp(current_epoch_time)
        HT = f"HUMAN TIME   : {converted_datetime}"
        TP = f"TIME POST       : {time_post}"
        app.post_result.insert("end", HT + '\n')
        app.post_result.insert("end", TP + '\n')
        app.post_result.insert("end", ' \n')
        print(HT)
        print(TP)

        json_payload = {
        "rq_id": 1234,
        "c_id": 1,
        "c_str": "sched",
        "data": {
            "cnt": 1,
            "scdl": [
            {
                "tst": schedule_time,
                "tqo": 3600000,
                "drn": 11000,
                "dps": 30000,
                "ftr": "null",
                "sid": "null"
            }
            ]
        }
        }
        for i in range(0, row):
            x = i + 1
            ID_COBOX = df.at[df.index[i],'ID COBOX']
            UUID = df.at[df.index[i],'UUID']
            topic_publish = f"aiot/cobox/{UUID}/command/request"
            json_message = json.dumps(json_payload)
            client.publish(topic_publish, json_message)
            content = f"{x}. ID COBOX = {ID_COBOX}"
            app.post_result.insert("end", content + '\n')
            time.sleep(1)
    except Exception:
        CTkMessagebox(title="Message",width=150,height=100,message="Something invalid",icon="assets/icon.png",option_1="ok")

def get_id_cobox(csv_file, UUID, column_to_return):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['UUID'] == UUID:
                return row[column_to_return]

def on_connect(client, userdata, flags, rc):
    print(f"STATUS MQTT  : result code {rc}")
    for topic in topic_response:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    try:
        json_data = json.loads(payload)
        res = str(json_data.get("rs_st"))
        sum_res.append(json_data)
        num = len(sum_res)
        # print(f"Received message on {msg.topic}: {json_data}")
        split = str(msg.topic).split("/")
        # print(split)
        res_uuid = split[2]
        COBOX = get_id_cobox(str(file_path), res_uuid, "ID COBOX")
        if res == "1":
            app.received_result.insert('end', str(num)+ '. ' + COBOX + ' Success' +'\n')
        else:
            app.received_result.insert('end', COBOX + ' Failed' +'\n')
    except json.JSONDecodeError as e:
        # print(f"Error decoding JSON: {e}")
        CTkMessagebox(title="Message",width=150,height=100,message="Something error",icon="assets/icon.png",option_1="ok")

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port, 60)
client.loop_start()

if __name__ == "__main__":
    app = App()
    app.mainloop()

    