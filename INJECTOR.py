import customtkinter,json,requests
from datetime import datetime
from CTkMessagebox import CTkMessagebox

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

url       = "http://192.168.4.1:2516/update"
url_test  = "http://192.168.4.1:2516/get"
ID        = ""

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("INJECTOR")
        self.iconbitmap('assets/iconx.ico')

        # configure grid layout
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # FRAME 1
        self.FR1 = customtkinter.CTkFrame(self, width=200, corner_radius=0, border_width=0)
        self.FR1.grid(row=0, column=3, rowspan=4, sticky="nsew")
        self.FR1.grid_rowconfigure(10, weight=1)
        
        self.mode_execute = customtkinter.CTkOptionMenu(self.FR1, width=180, values=["FIRMWARE","ID QC OPERATIONAL","ID PERFORMANCE TEST","ID PRODUCTION IKAN","ID PRODUCTION UDANG"])
        self.mode_execute.grid(row=0, column=0, padx=10, pady=10)
        self.mode_execute.set("MODE")

        self.test_connection = customtkinter.CTkButton(self.FR1, width=180, text="TEST CONNECTION", command=test_connection)
        self.test_connection.grid(row=1, column=0, padx=10, pady=10)

        self.input_ID = customtkinter.CTkEntry(self.FR1, width=180, placeholder_text="INPUT ID / FIRMWARE")
        self.input_ID.grid(row=2, column=0, padx=10, pady=10)

        self.execute_btn = customtkinter.CTkButton(self.FR1, width=180, text="EXECUTE", command=upload_file)
        self.execute_btn.grid(row=3, column=0, padx=10, pady=10)

        self.clear = customtkinter.CTkButton(self.FR1, width=180, text="CLEAR", command=clear_text_box)
        self.clear.grid(row=4, column=0, padx=10, pady=10)

        self.label = customtkinter.CTkLabel(self.FR1, text="mahesa.gilang@efishery.com", font=customtkinter.CTkFont(size=10))
        self.label.grid(row=5, column=0, columnspan=2, padx=0, pady=0, sticky="nsew")

        # FRAME 2
        self.FR2 = customtkinter.CTkFrame(self, width=0, corner_radius=0, border_width=0)
        self.FR2.grid(row=0, column=2, rowspan=4, sticky="nsew")
        self.FR2.grid_rowconfigure(10, weight=1)

        self.monitoring = customtkinter.CTkTextbox(self.FR2, width=230, height=250, corner_radius=10)
        self.monitoring.grid(row=0, column=0, rowspan=4, padx=10, pady=10, sticky="nsew")
        # sys.stdout = StdoutRedirector(self.monitoring)

def append_text_box(content):
    app.monitoring.insert("end", content + '\n')
    app.monitoring.see("end")  # Scroll to the end

def clear_text_box():
    app.monitoring.delete(0.0,"end")

def test_connection():
    try:
        requests.get(url_test,timeout=5)
    except Exception as e:
        CTkMessagebox(title="Message",width=150,height=100,message="WIFI NOT CONNECTED",icon="assets/icon.png",option_1="ok")

def upload_file():
    MODE = app.mode_execute.get()
    input = app.input_ID.get()
    if len(input) >= 1 and len(MODE) >= 5:
        time_now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        print(f"TIME   : {time_now}")
        print(f"MODE   : {MODE}")
        append_text_box(f"TIME : {time_now}")
        append_text_box(f"MODE : {MODE}")
        if MODE == "FIRMWARE":
            FW_file = f"FIRMWARE/firmware-v{app.input_ID.get()}.bin"
            with open(FW_file, 'rb') as file:
                files = {'file': (FW_file, file)}
                response = requests.post(url, files=files, timeout=90)
                json_data = json.loads(response.text)
                res = str(json_data.get("success"))
                print(f"RESULT : {res}")
                append_text_box(f"RESULT : {res}")
                append_text_box("============================")
        if MODE == "ID PRODUCTION IKAN":
            FS_file = f"ID PRODUCTION IKAN/ikan-fileSystem-efishery_{app.input_ID.get()}.bin"
            with open(FS_file, 'rb') as file:
                files = {'filesystem': (FS_file, file)}
                response = requests.post(url, files=files, timeout=90)
                json_data = json.loads(response.text)
                res = str(json_data.get("success"))
                print(f"RESULT : {res}")
                append_text_box(f"RESULT : {res}")
                append_text_box("============================")
        if MODE == "ID PRODUCTION UDANG":
            FS_file = f"ID PRODUCTION UDANG/udang-fileSystem-efishery_{app.input_ID.get()}.bin"
            with open(FS_file, 'rb') as file:
                files = {'filesystem': (FS_file, file)}
                response = requests.post(url, files=files, timeout=90)
                json_data = json.loads(response.text)
                res = str(json_data.get("success"))
                print(f"RESULT : {res}")
                append_text_box(f"RESULT : {res}")
                append_text_box("============================")
        if MODE == "ID PERFORMANCE TEST":
            FS_file = f"ID PERFORMANCE TEST/udang_mod2-fileSystem-efishery_{app.input_ID.get()}.bin"
            with open(FS_file, 'rb') as file:
                files = {'filesystem': (FS_file, file)}
                response = requests.post(url, files=files, timeout=90)
                json_data = json.loads(response.text)
                res = str(json_data.get("success"))
                print(f"RESULT : {res}")
                append_text_box(f"RESULT : {res}")
                append_text_box("============================")
        if MODE == "ID QC OPERATIONAL":
            FS_file = f"ID QC OPERATIONAL/udang-fileSystem-efishery_{app.input_ID.get()}.bin"
            with open(FS_file, 'rb') as file:
                files = {'filesystem': (FS_file, file)}
                response = requests.post(url, files=files, timeout=90)
                json_data = json.loads(response.text)
                res = str(json_data.get("success"))
                print(f"RESULT : {res}")
                append_text_box(f"RESULT : {res}")
                append_text_box("============================")
    else:
        CTkMessagebox(title="Message",width=150,height=100,message="INPUT IS EMPTY OR MODE HAS NOT BEEN SET ",icon="assets/icon.png",option_1="ok")

if __name__ == "__main__":
    app = App()
    app.mainloop()