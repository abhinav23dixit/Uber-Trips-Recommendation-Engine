import datetime
# datasets path
ratings_dataset_path = "Dataset/Rated User Interests.csv"
interests_dataset_path = "Dataset/Interests Dataset.csv"
users_dataset_path = "Dataset/Users Dataset.csv"
# threshold for getting top rated interests for a user
top_user_interests_limit = 3
OTHERS_REGEX = 'OTHERS'
# mocked places
PLACE_TYPE = [
    "RESTAURANT",
    "BAR",
    "GYM",
    "OFFICE",
    "PLAY ARENA",
    "SHOPPING",
    "OTHERS"
]
# mocked users
# 50 random users
USERS = [
    "Erika Brown",
    "John Peters",
    "Mark Rodriguez DDS",
    "Alexandra Lewis",
    "Michael Mckinney",
    "David Whitaker",
    "Steven Jones",
    "Patricia Marshall",
    "Rachel Williams",
    "Michelle Day",
    "John Medina",
    "Cynthia Campbell",
    "William Walker",
    "Kylie Gordon",
    "Margaret Brock",
    "Alexis Barry",
    "Richard Reid",
    "Kelly Torres",
    "Maria Tran",
    "David Hartman",
    "Heather Maxwell",
    "Amber Young",
    "Aaron Webb",
    "Nancy Brennan",
    "Heather Mcguire",
    "Brendan Rivera",
    "Elizabeth Gross",
    "David Rodriguez",
    "Samantha Coleman",
    "Courtney Jones",
    "Tracy Hanna",
    "Paul Smith",
    "Traci Braun",
    "Rose Cruz",
    "Ryan Barnes",
    "Sophia Hernandez",
    "David Patel",
    "Alexis Wang",
    "Jeremy Price",
    "William Jennings",
    "Sarah Peck",
    "Lance Chan",
    "Troy Stewart",
    "Alexandria Barrett",
    "George Thomas Jr.",
    "Chad Davis",
    "Wesley Wilson",
    "Lynn Elliott",
    "Matthew Russell",
    "Nicole Garrett"
]
# time classes
time_classes = {
    0: [datetime.time(0,0), datetime.time(2,59)],
    1: [datetime.time(3,0), datetime.time(5,59)],
    2: [datetime.time(6,0), datetime.time(8,59)],
    3: [datetime.time(9,0), datetime.time(11,59)],
    4: [datetime.time(12,0), datetime.time(14,59)],
    5: [datetime.time(15,0), datetime.time(17,59)],
    6: [datetime.time(18,0), datetime.time(20,59)],
    7: [datetime.time(21,0), datetime.time(23,59)]
}
