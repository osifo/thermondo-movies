from faker import Faker
from uuid import uuid4
from domain.user.model import User
from sqlalchemy.orm import Session
from sqlalchemy import insert
from pytest import fixture

def user():
  faker = Faker()
  firstname = faker.first_name()
  lastname = faker.last_name()
  email = faker.email()
  
  return {
    'firstname': firstname,
    'lastname': lastname,
    'email': email,
  }

async def create_user(db: Session):
  
  user_model = User(**user(), hashed_password='TESTpassword')
  db.add(user_model)
  db.commit()
  db.refresh(user_model)
  return user_model

async def create_users(db: Session, user_count=3):
  test_users = []

  for _ in range(user_count):
    test_users.append({
      **user(), 
      'hashed_password': 'TESTpassword',
      'id': str(uuid4())
    })

  db.execute(insert(User), test_users)
  db.commit()
