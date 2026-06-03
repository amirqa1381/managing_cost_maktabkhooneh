import os
import random
from locust import HttpUser, task, between
from locust.exception import StopUser

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.user_id = int(os.getenv("LOCUST_USER_ID", "1"))
        self.cost_ids = []
        username = os.getenv("LOCUST_USERNAME", "jack")
        password = os.getenv("LOCUST_PASSWORD", "jack")

        with self.client.post(
            "/user/login",
            data={"username": username, "password": password},
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"login failed: {response.text}")
                raise StopUser()

            token = response.json()["access_token"]

        self.client.headers.update({"Authorization": f"Bearer {token}"})

    def _cost_payload(self):
        amount = round(random.uniform(1, 500), 2)
        return {
            "user_id": self.user_id,
            "description": f"locust generated cost {amount}",
            "amount": str(amount),
        }

    def _create_cost(self):
        with self.client.post(
            "/costs",
            json=self._cost_payload(),
            name="/costs [create helper]",
            catch_response=True,
        ) as response:
            if response.status_code != 201:
                response.failure(f"create cost failed: {response.text}")
                return None

            cost_id = response.json()["id"]
            self.cost_ids.append(cost_id)
            return cost_id

    def _get_cost_id(self):
        if not self.cost_ids:
            return self._create_cost()

        return random.choice(self.cost_ids)

    @task
    def get_costs(self):
        self.client.get("/costs")

    @task
    def create_cost(self):
        self._create_cost()

    @task
    def update_cost(self):
        cost_id = self._get_cost_id()
        if cost_id is None:
            return

        amount = round(random.uniform(1, 500), 2)
        payload = {
            "description": f"locust updated cost {amount}",
            "amount": str(amount),
        }

        with self.client.put(
            f"/costs/{cost_id}",
            json=payload,
            name="/costs/{cost_id}",
            catch_response=True,
        ) as response:
            if response.status_code == 404 and cost_id in self.cost_ids:
                self.cost_ids.remove(cost_id)

    @task
    def delete_cost(self):
        cost_id = self._create_cost()
        if cost_id is None:
            return

        with self.client.delete(
            f"/costs/{cost_id}",
            name="/costs/{cost_id}",
            catch_response=True,
        ) as response:
            if response.status_code == 204 and cost_id in self.cost_ids:
                self.cost_ids.remove(cost_id)
