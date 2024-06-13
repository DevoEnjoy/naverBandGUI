# -*- coding: utf-8 -*-
# v240322
import os
import sys
import yaml
# import naverBandAPI.client as client
from __init__ import config_file_path, root_folder_path
sys.path.append(root_folder_path)
from library.basic import *
from crawling import Crawling

import tkinter as tk
from tkinter import ttk
from cryptography.fernet import Fernet
import os
import time
import pyautogui
import pyperclip

class BandGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("NaverBandGUI - Controller")
        
        self.notebook = ttk.Notebook(root, width=300, height=450)
        self.notebook.pack()
        
        # Create the main frame
        self.login_frame = ttk.Frame(self.root)
        # self.login_frame.grid()
        
        self.search_frame = ttk.Frame(self.root, padding="10 10 10 10")
        # self.search_frame.grid()

        self.key = self.load_key()
        self.cipher = Fernet(self.key)
        
        self.login_options = [
            # "이메일",
            "네이버",
            # "페이스북",
            # "애플",
        ]

        # Create and place widgets
        self.setting_login()
        
        self.setting_search()
        
        self.notebook.add(self.login_frame, text="로그인")
        self.notebook.add(self.search_frame, text="검색")
        
        self.load_credentials()
        
        self.logins = [
            # self.login_email, 
            self.login_naver, 
            # self.login_facebook, 
            # self.login_apple
        ]
        
        self.crawl = Crawling(url="https://band.us/home")
        self.crawl.run()
    
    def setting_login(self):
        # ID Label and Entry
        self.id_label = ttk.Label(self.login_frame, text="ID:")
        self.id_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.id_entry = ttk.Entry(self.login_frame, width=20)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Password Label and Entry
        self.password_label = ttk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.password_entry = ttk.Entry(self.login_frame, width=20, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Remember Me Checkbox
        self.remember_var = tk.BooleanVar()
        self.remember_check = ttk.Checkbutton(self.login_frame, text="Remember Me", variable=self.remember_var)
        self.remember_check.grid(row=2, columnspan=2, padx=5, pady=5)
        
        # Login Options
        self.login_option_label = ttk.Label(self.login_frame, text="Login Options:")
        self.login_option_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

        self.login_option_var = tk.StringVar()
        
        self.login_option_combobox = ttk.Combobox(self.login_frame, textvariable=self.login_option_var, values=self.login_options, state="readonly")
        self.login_option_combobox.grid(row=3, column=1, padx=5, pady=5)
        self.login_option_combobox.current(0)  # Default option
        
        # Login Button
        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=4, column=1, padx=5, pady=5, sticky=tk.E)
        self.login_frame.pack()
        
        
    def setting_search(self):
        # Navigate Button
        self.navigate_button = ttk.Button(self.search_frame, text="Go to Band main", command=self.navigate)
        self.navigate_button.grid(row=5, column=1, padx=5, pady=5, sticky=tk.E)
        
        # Search Term Label and Entry
        self.search_label = ttk.Label(self.search_frame, text="Search Term:")
        self.search_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.search_entry = ttk.Entry(self.search_frame, width=20)
        self.search_entry.grid(row=6, column=1, padx=5, pady=5)
        
        # Start Crawling Button
        self.crawl_button = ttk.Button(self.search_frame, text="Start Crawling", command=self.start_crawling)
        self.crawl_button.grid(row=7, column=1, padx=5, pady=5, sticky=tk.E)
        
        
        self.scrollbar = ttk.Scrollbar(self.search_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(self.search_frame, selectmode=tk.MULTIPLE, yscrollcommand=self.scrollbar.set)
        self.listbox.pack()
        self.scrollbar.config(command=self.listbox.yview)
        
        




        self.search_frame.pack()
        
    def update_listbox(self, items):
        self.listbox.delete(0, tk.END)
        for item in items:
            self.listbox.insert(tk.END, item)
        
    def load_key(self):
        key_file = 'secret.key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as file:
                key = file.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as file:
                file.write(key)
        return key

    def save_credentials(self, user_id, password, login_option):
        credentials = f"{user_id}:{password}:{login_option}".encode()
        encrypted_credentials = self.cipher.encrypt(credentials)
        with open('credentials.enc', 'wb') as file:
            file.write(encrypted_credentials)
    
    def load_credentials(self):
        if os.path.exists('credentials.enc'):
            with open('credentials.enc', 'rb') as file:
                encrypted_credentials = file.read()
            decrypted_credentials = self.cipher.decrypt(encrypted_credentials).decode()
            user_id, password, login_option = decrypted_credentials.split(':')
            self.id_entry.insert(0, user_id)
            self.password_entry.insert(0, password)
            self.login_option_var.set(login_option)
            self.remember_var.set(True)

    def login(self):
        user_id = self.id_entry.get()
        password = self.password_entry.get()
        login_option = self.login_option_var.get()
        # print(f"Logging in with ID: {user_id}, Password: {password}, Login Option: {login_option}")
        if self.remember_var.get():
            self.save_credentials(user_id, password, login_option)
        else:
            if os.path.exists('credentials.enc'):
                os.remove('credentials.enc')
        
        selected_login_option = self.login_options.index(login_option)
        
        self.logins[selected_login_option](user_id, password)
        
    def login_email(self, user_id, password):
        self.crawl.set_url(url="https://auth.band.us/email_login")
        wait = self.crawl.run(10)
        
        # wait.until()
        
        input_email = self.crawl.find_element("id", "input_email")
        input_email.send_keys(user_id)
        
        submit_btn = self.crawl.find_element("tag", "button")
        submit_btn.click()
        
        input_pw = self.crawl.find_element("id", "pw")
        input_pw.send_keys(password)
        
        submit_btn2 = self.crawl.find_element("class", "-confirm")
        submit_btn2.click()
        
    def login_naver(self, user_id, password):
        self.crawl.set_url(url="https://nid.naver.com/")
        self.crawl.run(3)
        
        input_id = self.crawl.find_element("css_selector", "#id")
        # input_pw.send_keys(user_id)
        print("id 클릭")
        input_id.click()
        pyperclip.copy(user_id)
        pyautogui.hotkey("ctrl", "v")
        print("아이디 입력")
        time.sleep(1)
        
        input_pw = self.crawl.find_element("css_selector", "#pw")
        # input_pw.send_keys(password)
        print("pw 클릭")
        input_pw.click()
        time.sleep(1)
        pyperclip.copy(password)
        pyautogui.hotkey("ctrl", "v")
        print("비번 입력")
        time.sleep(1)
        
        self.crawl.find_element("css_selector", "#login_keep_wrap > div.keep_check > label").click()
        time.sleep(1)
        
        self.crawl.find_element("css_selector", "#login_keep_wrap > div.ip_check > span > label").click()
        time.sleep(1)
        
        submit_btn = self.crawl.find_element("id", "log.login")
        submit_btn.click()
        time.sleep(1)
        print("로그인 클릭")
        
        self.crawl.set_url(url="https://auth.band.us/")
        self.crawl.run(2)
        
        # keep login click
        self.crawl.find_element("css_selector", "#content > div > label").click()
        print("로그인 유지")
        time.sleep(1)
        
        # naver login click
        self.crawl.find_element("css_selector", "#login_list > li:nth-child(3) > a").click()
        print("밴드 로그인")
        
        
    def login_facebook(self, user_id, password):
        
        pass
    
    def login_apple(self, user_id, password):
        
        pass
    
    def navigate(self):
        self.crawl.set_url("https://band.us/").run(2)

    def start_crawling(self):
        search_term = self.search_entry.get()
        
        # 검색창 클릭
        self.crawl.find_element("css_selector", "#input_search_view64").click()
        pyperclip.copy(search_term)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(2)
        
        # 검색버튼 클릭
        self.crawl.find_element("css_selector", "#btn_search").click()
        time.sleep(3)
        
        self.update_listbox(self.get_band_links())
        
    def get_band_links(self):
        elements = self.driver.find_elements_by_class_name("_goBand")
        return [elem.get_attribute("href") for elem in elements]

if __name__ == "__main__":
    root = tk.Tk()
    app = BandGUI(root)
    root.mainloop()
