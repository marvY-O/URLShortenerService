from locust import HttpUser, task, between
from pandas import read_csv
import random

class MyUser(HttpUser):
    wait_time = between(1, 3)  # Wait time between tasks in seconds
    
    short_urls = None

    def load_data_from_csv(self, csv_file, column):
        urls_df = read_csv(csv_file)
        return urls_df[column].values

    def on_start(self):
        # Load the data from the CSV file when the user starts
        if MyUser.short_urls is None:
            MyUser.short_urls = set(self.load_data_from_csv('short_urls.csv', 'short_url'))

    @task(1)
    def write_requests(self):
        urls = self.load_data_from_csv('urls.csv', 'url')

        endpoint = "http://127.0.0.1:8000/shorten/"
        headers = {
            "Content-Type": "application/json"
        }
        
        for i in range(10):

            r_idx = random.randrange(0, len(urls))
            payload = {
                "long_url": urls[r_idx]
            }

            response = self.client.post(endpoint, json=payload, headers=headers)
            short_url = response.json()['short_url']
            if MyUser.short_urls is not None:
                MyUser.short_urls.add(short_url)
                
            print(f"Response: {response.status_code} - {response.text}")

        self.interrupt()

    @task(1)
    def read_requests(self):
        urls = self.load_data_from_csv('urls.csv', 'url')

        endpoint = "http://127.0.0.1:8000/"

        if MyUser.short_urls is not None:
            random_short_urls = random.sample(MyUser.short_urls, 100)
            for short_url in random_short_urls:
                with self.client.get(endpoint+short_url, catch_response=True) as response:
                    print(f"Response: {response.status_code}")

        self.interrupt()