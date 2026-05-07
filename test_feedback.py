import paho.mqtt.client as mqtt
import os

# Lấy thông tin từ GitHub Secrets để bảo mật
MQTT_SERVER = os.getenv('f7a99425c8a34f23aba171e48336da3b.s1.eu.hivemq.cloud')
MQTT_USER = os.getenv('long140203')
MQTT_PASS = os.getenv('Long140203')

def send_response():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.tls_set() # Dùng kết nối bảo mật
    
    try:
        client.connect(MQTT_SERVER, 8883)
        # Gửi tin nhắn xác nhận về cho Web
        client.publish("web/test/response", "Code Python đã phản hồi thành công! Đèn đã bật (giả lập).")
        print("Đã gửi phản hồi về Web!")
        client.disconnect()
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    send_response()
