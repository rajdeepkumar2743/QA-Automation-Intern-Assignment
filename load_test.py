from locust import HttpUser, TaskSet, task, between

# TaskSet defining user behavior
class UserBehavior(TaskSet):
    @task
    def get_users(self):
        """
        Simulates a user requesting the list of users on page 2.
        """
        self.client.get("/api/users?page=2")

# HttpUser class defining load test configuration
class WebsiteUser(HttpUser):
    tasks = [UserBehavior]  # Assign behavior/tasks to the virtual user
    wait_time = between(1, 5)  # Wait time between tasks (in seconds)
