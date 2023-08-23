from locust import HttpUser, task, between
from pandas import read_csv

class MyUser(HttpUser):
    wait_time = between(1, 3)  # Wait time between tasks in seconds

    def load_data_from_csv(self, csv_file):
        urls_df = read_csv(csv_file)
        return urls_df['url'].values

    @task(1)
    def my_task(self):
        urls = self.load_data_from_csv('urls.csv')

        endpoint = "http://127.0.0.1:8000/shorten/"
        headers = {
            "Content-Type": "application/json"
        }
        
        for i in range(10000):

            payload = {
                "long_url": urls[i]
            }

            response = self.client.post(endpoint, json=payload, headers=headers)

            print(f"Response {i}: {response.status_code} - {response.text}")
        
        self.environment.runner.stop()

