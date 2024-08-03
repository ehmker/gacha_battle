import time
import psycopg
import os
import threading
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class Database():
    def __init__(self, timeout=10) -> None:
        self.connection = None
        self.last_used = time.time()
        self.timeout = timeout
        self.connect()
        self.start_timeout_checker()
        
    def connect(self):
        try:
            self.connection = psycopg.connect(f"host=localhost dbname={os.getenv("POSTGRES_DB")} user={os.getenv("POSTGRES_USER")} password={os.getenv("POSTGRES_PASSWORD")}")
            self.last_used = time.time()
            print(f'Connected to Database @ {datetime.fromtimestamp(self.last_used)}')
        except psycopg.Error as e:
            print(f'error connecting to database: {e}')
        
        
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print('database disconnected')
            
    def start_timeout_checker(self):
        def check_timeout():
            while True:
                if self.connection and (time.time() - self.last_used > self.timeout):
                    self.close()
                time.sleep(10)
                
        # start timeout checker on separate thread 
        threading.Thread(target=check_timeout, daemon=True).start()
        
        
    def get_user_info_by_id(self, user_id):
        self._check_connection()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                           SELECT *
                           FROM users
                           WHERE id = %s
                           ''', (user_id,))
            user_info = cursor.fetchone()
            cursor.close()
            return user_info
        except psycopg.Error as e:
            print(f'error fetching user info data: {e}')
            return None
        
    def get_user_info_by_name(self, username):
        self._check_connection()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                           SELECT *
                           FROM users
                           WHERE username = %s
                           ''', (username,))
            user_info = cursor.fetchone()
            cursor.close()
            return user_info
        except psycopg.Error as e:
            print(f'error fetching user info data: {e}')
            return None
        
    def add_new_user(self, username):
        self._check_connection()
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                           INSERT INTO users (username)
                           VALUES(%s)
                           ''', (username,))
            self.connection.commit()
            cursor.close()
            print(f'User added: {username}')
        except psycopg.Error as e:
            print(f'error adding user: {e}')
            
            
    
    def _check_connection(self):
        if self.connection is None:
            self.connect()
        self.last_used = time.time()

    def load_init_file(self, file):
        self._check_connection()
        try:
            with open(file, 'r') as f:
                cursor = self.connection.cursor()
                cursor.execute(f.read())
                self.connection.commit()
                cursor.close()
                print()
        except psycopg.Error as e:
            print(f'error adding user: {e}')
