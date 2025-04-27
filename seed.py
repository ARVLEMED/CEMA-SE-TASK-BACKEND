from datetime import datetime
from app import app, db
from models import Client, Program, Enrollment, Consultation, User

def seed_database():
    # Create a Flask application context
    with app.app_context():
        # Delete existing data (except users)
        db.session.query(Consultation).delete()
        db.session.query(Enrollment).delete()
        db.session.query(Program).delete()
        db.session.query(Client).delete()
        db.session.commit()

        # Check if user_id=1 exists
        default_user = User.query.get(1)
        if not default_user:
            print("Error: User with id=1 does not exist. Please create a user first.")
            return

        # Seed Clients
        client1 = Client(name="Alice Smith", age=34, status="Active")
        client2 = Client(name="Bob Johnson", age=45, status="Waiting")
        client3 = Client(name="Clara Davis", age=28, status="Active")
        client4 = Client(name="David Wilson", age=52, status="Inactive")
        client5 = Client(name="Emma Brown", age=19, status="Active")
        client6 = Client(name="Frank Miller", age=63, status="Waiting")
        db.session.add_all([client1, client2, client3, client4, client5, client6])
        db.session.commit()

        # Seed Programs
        program1 = Program(
            user_id=1,
            name="Weight Loss Program",
            description="A 12-week program focused on healthy weight loss."
        )
        program2 = Program(
            user_id=1,
            name="Diabetes Management",
            description="A program to help manage diabetes through diet and exercise."
        )
        program3 = Program(
            user_id=1,
            name="TB Clinic",
            description="A program for tuberculosis treatment and follow-up."
        )
        program4 = Program(
            user_id=1,
            name="Cardiac Care",
            description="A program for heart health and recovery."
        )
        program5 = Program(
            user_id=1,
            name="Mental Health Support",
            description="A program offering counseling and stress management."
        )
        db.session.add_all([program1, program2, program3, program4, program5])
        db.session.commit()

        # Seed Enrollments
        enrollment1 = Enrollment(client_id=client1.id, program_id=program1.id)
        enrollment2 = Enrollment(client_id=client1.id, program_id=program4.id)
        enrollment3 = Enrollment(client_id=client2.id, program_id=program2.id)
        enrollment4 = Enrollment(client_id=client3.id, program_id=program1.id)
        enrollment5 = Enrollment(client_id=client3.id, program_id=program5.id)
        enrollment6 = Enrollment(client_id=client4.id, program_id=program3.id)
        enrollment7 = Enrollment(client_id=client5.id, program_id=program2.id)
        enrollment8 = Enrollment(client_id=client6.id, program_id=program4.id)
        db.session.add_all([enrollment1, enrollment2, enrollment3, enrollment4, enrollment5, enrollment6, enrollment7, enrollment8])
        db.session.commit()

        # Seed Consultations
        consultation1 = Consultation(
            client_id=client1.id,
            vitals="BP 120/80, HR 70",
            allergies="Peanuts",
            symptoms="Fatigue, headache",
            medical_history="History of migraines",
            medications="Ibuprofen as needed",
            diagnosis="Possible migraine",
            investigations="Blood test ordered",
            treatment_plan="Rest, hydration, follow-up in 1 week"
        )
        consultation2 = Consultation(
            client_id=client2.id,
            vitals="BP 130/85, HR 75",
            allergies="None",
            symptoms="Increased thirst, frequent urination",
            medical_history="Family history of diabetes",
            medications="None",
            diagnosis="Suspected Type 2 Diabetes",
            investigations="Fasting glucose test ordered",
            treatment_plan="Monitor blood sugar, dietary changes"
        )
        consultation3 = Consultation(
            client_id=client3.id,
            vitals="BP 115/75, HR 68",
            allergies="Pollen",
            symptoms="Weight gain, low energy",
            medical_history="None",
            medications="None",
            diagnosis="Possible thyroid issue",
            investigations="Thyroid function test ordered",
            treatment_plan="Increase physical activity, follow-up in 2 weeks"
        )
        consultation4 = Consultation(
            client_id=client4.id,
            vitals="BP 140/90, HR 80",
            allergies="Dust",
            symptoms="Chest pain, shortness of breath",
            medical_history="Hypertension",
            medications="Amlodipine 5mg",
            diagnosis="Possible angina",
            investigations="ECG ordered",
            treatment_plan="Refer to cardiologist, avoid strenuous activity"
        )
        consultation5 = Consultation(
            client_id=client5.id,
            vitals="BP 110/70, HR 72",
            allergies="None",
            symptoms="Anxiety, trouble sleeping",
            medical_history="None",
            medications="None",
            diagnosis="Generalized anxiety disorder",
            investigations="None",
            treatment_plan="Refer to mental health program, consider counseling"
        )
        consultation6 = Consultation(
            client_id=client6.id,
            vitals="BP 135/88, HR 65",
            allergies="Shellfish",
            symptoms="Cough, weight loss",
            medical_history="Smoker",
            medications="None",
            diagnosis="Suspected TB",
            investigations="Chest X-ray ordered",
            treatment_plan="Refer to TB Clinic, isolate until results"
        )
        db.session.add_all([consultation1, consultation2, consultation3, consultation4, consultation5, consultation6])
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()