from locust import HttpUser, TaskSet, task, between
from faker import Faker
import random

fake = Faker()

class UserBehavior(TaskSet):
    @task
    def submit_form(self):
        # Datos del formulario generados aleatoriamente
        form_data = {
            'birth_year': random.randint(1950, 2010),
            'gender': random.choice(['Male', 'Female', 'Other']),
            'textura': random.choice(['Suave', 'Rugosa', 'Fina', 'Gruesa']),
            'consistencia': random.randint(1, 5),
            'satisfactionRange': random.randint(1, 5),
            'satisfactionRange_4': random.randint(1, 5),
            'satisfactionRange_5': random.randint(1, 5),
            'humedad': random.choice(['Alta', 'Media', 'Baja']),
            'sabores': random.choice(['Dulce', 'Salado', 'Amargo', 'Ácido']),
            'respuesta7': fake.sentence()
        }
        
        self.client.post("/submit", data=form_data)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)

if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py --host http://localhost:8000")

