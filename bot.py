import os
import time
import openai
from instagrapi import Client

# Ambil variabel dari environment
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
IG_USERNAME = os.environ["IG_USERNAME"]
IG_PASSWORD = os.environ["IG_PASSWORD"]

# Inisialisasi OpenAI Client
openai.api_key = OPENAI_API_KEY

def get_ai_reply(message):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",  # Pilih model yang ingin digunakan
            prompt=message,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"❌ Error AI: {e}")
        return "Maaf, aku lagi error nih!"

# Inisialisasi Instagram Client
cl = Client()

def login_instagram():
    try:
        cl.login(IG_USERNAME, IG_PASSWORD)
        print("✅ Login Instagram berhasil!")
    except Exception as e:
        print(f"❌ Gagal login: {e}")

def send_message():
    try:
        # Ambil thread pesan masuk dari Instagram
        inbox = cl.direct_threads()
        for thread in inbox:
            last_message = thread.messages[0].text
            if last_message:
                print(f"📩 Pesan masuk: {last_message}")
                reply = get_ai_reply(last_message)
                cl.direct_send(reply, thread_id=thread.id)
                print(f"✉️ Balas: {reply}")
            time.sleep(1)  # Tunggu 1 detik untuk mengirim pesan berikutnya
    except Exception as e:
        print(f"❌ Error di auto-reply: {e}")

if __name__ == "__main__":
    login_instagram()
    
    # Loop untuk menjalankan pengiriman pesan setiap detik selama 60 detik (1 menit)
    start_time = time.time()
    while True:
        send_message()
        time.sleep(1)  # Tunggu 1 detik sebelum melanjutkan ke langkah berikutnya
        if time.time() - start_time >= 60:  # Batasi pengiriman pesan hingga 60 detik
            break
            
