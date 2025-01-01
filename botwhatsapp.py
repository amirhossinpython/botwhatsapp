import pyautogui
import time
import requests
import pyperclip  # برای کپی کردن به کلیپ‌بورد
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext

def get_response_from_api(user_input):
    url = "https://api.api-code.ir/gpt-4/"
    payload = {"text": user_input}

    try:
        response = requests.get(url, params=payload)
        response.raise_for_status()  

        data = response.json()
        return data['result']  

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"Request error occurred: {req_err}"
    except Exception as e:
        return f"An error occurred: {e}"

def save_response_to_file(response):
    # ذخیره پاسخ در فایل متنی
    with open("response.txt", "w", encoding="utf-8") as file:
        file.write(response + "\n")  # اضافه کردن پاسخ به فایل

def copy_text_to_clipboard():
    # خواندن محتوای فایل و کپی کردن آن به کلیپ‌بورد
    try:
        with open("response.txt", "r", encoding="utf-8") as file:
            file_content = file.read()  # خواندن محتوای فایل
        pyperclip.copy(file_content)  # کپی محتوا به کلیپ‌بورد
        return "محتوا به کلیپ‌بورد کپی شد."
    except Exception as e:
        return f"خطا در خواندن فایل: {e}"

def send_message_to_whatsapp():
    # چسباندن محتویات کلیپ‌بورد به واتساپ و ارسال آن
    pyautogui.hotkey('ctrl', 'v')  # چسباندن محتویات کلیپ‌بورد
    time.sleep(1)  # تأخیر برای اطمینان از چسباندن کامل
    pyautogui.press('enter')  # ارسال پیام
    time.sleep(1)

def handle_request():
    user_input = input_text.get("1.0", tk.END).strip()
    if not user_input:
        messagebox.showwarning("هشدار", "لطفاً سوال خود را وارد کنید!")
        return

    status_label.config(text="در حال دریافت پاسخ از وب‌سرویس...")
    response = get_response_from_api(user_input)
    
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, response)

    save_response_to_file(response)
    copy_message = copy_text_to_clipboard()
    status_label.config(text=copy_message)

    send_message_to_whatsapp()
    status_label.config(text="پاسخ ارسال شد.")

def create_gui():
    global input_text, output_text, status_label

    # ایجاد پنجره اصلی
    root = tk.Tk()
    root.title("ربات واتساپ ")
    root.geometry("500x600")

    # برچسب ورودی
    tk.Label(root, text="سوال خود را وارد کنید:", font=("Arial", 12)).pack(pady=10)

    # کادر متنی برای ورودی
    input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=5, font=("Arial", 12))
    input_text.pack(pady=10)

    # دکمه ارسال
    tk.Button(root, text="دریافت و ارسال", font=("Arial", 12), command=handle_request).pack(pady=10)

    # کادر متنی برای نمایش خروجی
    tk.Label(root, text="پاسخ دریافت‌شده:", font=("Arial", 12)).pack(pady=10)
    output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10, font=("Arial", 12))
    output_text.pack(pady=10)

    # برچسب وضعیت
    status_label = tk.Label(root, text="وضعیت: آماده", font=("Arial", 10), fg="green")
    status_label.pack(pady=10)

    # شروع حلقه اصلی
    root.mainloop()

if __name__ == "__main__":
    create_gui()
