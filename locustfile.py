from locust import HttpLocust, TaskSet, task
import sys

# This will first make a POST to /tokenEndpoint, followed by a GET to /account using part of the response returned from /tokenEndpoint.
# Each locust would have a unique userid starting at 1
# Command: locust -f [filename] --host=[hostname]

Globalid = 0

class UserBehavior(TaskSet):
	userid = "NOT_FOUND"
	token = "NOT_FOUND"
	LoginParam = {
		"pw": "password"
	}

	def on_start(self):
		global Globalid
		Globalid += 1
		self.userid = str(Globalid)

	def on_stop(self):
		global Globalid
		Globalid = 0

	@task
	def login(self):
		LoginBody = {
			"key": "value"
		}
		with self.client.post("/tokenEndpoint", json=LoginBody, params=self.LoginParam, name="/tokenEndpoint", catch_response=True) as r:
			response = r.json()
			if 'err' in response:
				failureString = "Error in response. Err: {}".format(response['err'])
				r.failure(failureString)
				return
			if not 'token' in response:
				failureString = "Response does not contain token key."
				r.failure(failureString)
				return
			self.token = response['token']

		AccountParam = {
			"token": self.token
		}
		with self.client.get("/account", params=AccountParam, name="/account", catch_response=True) as r2:
			response2 = r2.json()
			if 'err' in response2:
				failureString = "Error in result. Err: {}".format(response2['err'])
				r2.failure(failureString)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
