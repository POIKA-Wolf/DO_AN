import paho.mqtt.client as mqtt
import random
import os

# Cấu hình MQTT từ GitHub Secrets
MQTT_SERVER = "f7a99425c8a34f23aba171e48336da3b.s1.eu.hivemq.cloud"
MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASS = os.getenv('MQTT_PASS')

def run_ga_optimization():
    # Giả lập dữ liệu thời tiết & ánh sáng (có thể dùng API OpenWeatherMap)
    light_val = 700  # Lux
    temp_weather = 30 # Độ C
    
    # Mục tiêu: Tìm Setpoint độ ẩm (x) tối ưu
    # Giả sử lý tưởng: Nếu trời nóng & sáng mạnh -> cần độ ẩm cao hơn
    ideal_humidity = 50 + (temp_weather * 0.5) + (light_val * 0.01)
    
    population = [random.uniform(40, 90) for _ in range(50)]
    
    for generation in range(100):
        # Sắp xếp theo độ lệch so với giá trị lý tưởng
        population.sort(key=lambda x: abs(x - ideal_humidity))
        # Lai ghép & Đột biến đơn giản
        parents = population[:10]
        population = parents + [p + random.uniform(-1, 1) for p in parents for _ in range(4)]
        
    return round(population[0], 2)

def publish_setpoint(val):
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.tls_set()
    client.connect(MQTT_SERVER, 8883)
    client.publish("esp8266/setpoint", str(val))
    client.disconnect()

if __name__ == "__main__":
    result = run_ga_optimization()
    print(f"Optimal Setpoint found: {result}")
    publish_setpoint(result)
