# seed.py
from app.database import SessionLocal, engine
import app.models as models

# Create all tables
models.Base.metadata.create_all(bind=engine)

# Seed data
def seed_data():
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(models.Sweet).count() == 0:
            sweets = [
                models.Sweet(name="Chocolate Bar", category="candy", price=20, quantity=50),
                models.Sweet(name="Gulab Jamun", category="indian", price=15, quantity=30),
                models.Sweet(name="Ladoo", category="indian", price=10, quantity=40),
                models.Sweet(name="Jelly Beans", category="candy", price=5, quantity=100),
            ]
            db.add_all(sweets)
            db.commit()
            print("✅ Database seeded successfully!")
        else:
            print("⚡ Data already exists, skipping seeding.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
