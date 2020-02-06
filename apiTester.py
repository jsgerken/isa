# equivalent of curl -d "param1=value1&param2=value2" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://localhost:8001/api/v1/users/1
import requests

#  email = models.CharField(max_length = 50, unique=True)
#     username = models.CharField(max_length = 50, unique = True)
#     password = models.CharField(max_length = 50)
#     phone_number = models.CharField(max_length = 14)
#     first_name = models.CharField(max_length = 30)
#     last_name = models.CharField(max_length = 30)
#     is_deleted = models.BooleanField(False)
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = {
    'email': "newUser1@virginia.edu",
    'username': "TestJay",
    'password': "12345",
    'phone_number': "123-455-3456",
    'first_name': 'NotTA',
    'last_name': 'Jay',
    # 'is_deleted': 'false'

}

response = requests.post(
    'http://localhost:8001/api/v1/users/create/', headers=headers, data=data)

print(response.json())
