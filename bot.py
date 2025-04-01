import os
import time
import openai
from instagrapi import Client

# Menambahkan print untuk debugging
print("Bot lagi jalan . . .")  # Tambahkan print di sini

# Ambil variabel dari environment
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
IG_USERNAME = os.environ["IG_USERNAME"]
IG_PASSWORD = os.environ["IG_PASSWORD"]

# Inisialisasi OpenAI Client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_ai_reply(message):
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
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

def auto_reply():
    try:
        inbox = cl.direct_threads()
        for thread in inbox:
            last_message = thread.messages[0].text
            if last_message:
                reply = get_ai_reply(last_message)
                cl.direct_send(reply, thread_id=thread.id)
                print(f"📩 Balas: {last_message} ➜ {reply}")
            time.sleep(2)
    except Exception as e:
        print(f"❌ Error di auto-reply: {e}")

if __name__ == "__main__":
    print("Starting Instagram bot...")  # Tambahkan print lagi di sini
    login_instagram()
    auto_reply()
    
