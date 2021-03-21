import csv
from faker import Faker

faker = Faker()
for n in range(50):
    print(faker.name())

# import pandas as pd
# def load_dataset(path):
#     dataset = pd.read_csv(path)
#     dataset.head()


# load_dataset("My Uber Drives - 2016.csv")