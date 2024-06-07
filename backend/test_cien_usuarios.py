from locust import HttpUser, task, between
import random

class UserBehavior(HttpUser):
    wait_time = between(1, 5)
    host = "http://127.0.0.1:8000"  # Especifica el host aquí

    @task
    def submit_form(self):
        data = self.generate_random_data()
        self.client.post("/submit", data=data)

    def generate_random_data(self):
        birth_year = random.randint(1960, 2020)
        gender = random.choice(["male", "female", "other"])
        textura = random.choice(["suave", "rugosa", "crujiente"])
        consistencia = random.choice(["firme", "blanda", "líquida"])
        chocolate = random.choice(["amargo", "dulce", "semidulce"])
        atraccion = random.choice(["alta", "media", "baja"])
        expectativa = random.choice(["alta", "media", "baja"])
        humedad = random.choice(["seca", "húmeda", "muy húmeda"])
        sabores = random.choice(["intenso", "moderado", "suave"])
        respuesta7 = random.choice(["sí", "no", "quizás"])

        return {
            "birth_year": birth_year,
            "gender": gender,
            "textura": textura,
            "consistencia": consistencia,
            "chocolate": chocolate,
            "atraccion": atraccion,
            "expectativa": expectativa,
            "humedad": humedad,
            "sabores": sabores,
            "respuesta7": respuesta7
        }
