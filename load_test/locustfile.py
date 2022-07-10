from locust import FastHttpUser, task, between


class FlandriaUser(FastHttpUser):
    wait_time = between(1, 5)

    @task
    def root(self):
        self.client.get("/")

    @task
    def static_pages(self):
        self.client.get("/about")
        wait_time = between(1, 5)
        self.client.get("/privacy-policy")
        wait_time = between(1, 5)
        self.client.get("/legal-notice")
