from locust import HttpUser, task, between
from queue import Queue, Empty
import random
from locust.exception import StopUser
from datetime import datetime, timedelta, timezone

def generate_booking_dates():
    start_offset = random.randint(1, 30)
    check_in = datetime.now(tz=timezone.utc) + timedelta(days=start_offset)
    
    duration = random.randint(1, 10)
    check_out = check_in + timedelta(days=duration)
    
    check_in_str = check_in.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
    check_out_str = check_out.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'

    return check_in_str, check_out_str



USER_CREDENTIALS = Queue()
for i in range(3, 395):
    USER_CREDENTIALS.put({"email": f"user{i}@example.com", "password": f"user{i}"})

class ApiUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
    
        try:

            user_data = USER_CREDENTIALS.get_nowait()


        except Empty:
            print("No users more")
            raise StopUser()
        
        response = self.client.post("/v1/auth/login", json=user_data)
        if response.status_code == 200:
            token = response.json().get("jwt_token")
            self.client.headers.update({"Authorization": f"Bearer {token}"})


    @task(3)
    def get_hotel_by_id(self):
        random_room_id = random.randint(2, 400)

        self.client.get(f"/v1/rooms/{random_room_id}")

    @task(1)
    def make_booking(self):
        random_room_id = random.randint(2, 400)
        check_in, check_out = generate_booking_dates()
        payload = {
            "room_id" : random_room_id,
            "check_in" : check_in,
            "check_out" : check_out
        }

        with self.client.post(url=f"/v1/bookings/", json=payload, catch_response=True) as response:

            if response.status_code == 200:
                response.success()
            elif response.status_code == 422:
                response.failure(f"Validation error: {response.text}")
            elif response.status_code == 409:
                response.success()
            else:
                response.failure(f"Status {response.status_code}")