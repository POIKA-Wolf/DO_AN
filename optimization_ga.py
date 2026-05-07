import paho.mqtt.client as mqtt
import requests
import random

# Cấu hình HiveMQ
MQTT_SERVER = "f7a99425c8a34f23aba171e48336da3b.s1.eu.hivemq.cloud"
MQTT_USER = "long140203"
MQTT_PASS = "Long140203"

def get_weather_data():
    # Giả lập lấy dữ liệu từ OpenWeather API
    # Dữ liệu thực tế: Ánh sáng mạnh + Nhiệt độ cao -> Cần SetPoint ẩm cao hơn
    return {"temp_outside": 32, "light_intensity": 800}

def genetic_algorithm(weather):
    # Hàm fitness: Tìm độ ẩm sao cho cây không bị héo và tiết kiệm nước
    # Đầu ra là 1 giá trị SetPoint từ 50% - 85%
    population = [random.uniform(50, 85) for _ in range(20)]
    for _ in range(10): # Chạy 10 thế hệ
        # Logic chọn lọc dựa trên dữ liệu thời tiết
        population = sorted(population, key=lambda x: abs(x - (weather['temp_outside'] * 2)))
    return round(population[0], 2)

def on_connect(client, userdata, flags, rc):
    client.subscribe("esp8266/control/ga")

def on_message(client, userdata, msg):
    if msg.payload.decode() == "START_GA":
        print("Đang chạy thuật toán GA...")
        weather = get_weather_data()
        optimal_setpoint = genetic_algorithm(weather)
        # Gửi SetPoint về cho ESP32
        client.publish("esp8266/setpoint", str(optimal_setpoint))
        print(f"Đã gửi SetPoint tối ưu: {optimal_setpoint}")

client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set()
client.connect(MQTT_SERVER, 8883)
client.loop_forever()
