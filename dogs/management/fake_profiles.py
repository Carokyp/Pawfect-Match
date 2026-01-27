from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import OwnerProfile
from dogs.models import Dog


class Command(BaseCommand):
    help = "fake dog & owner profiles for prototype"

    def handle(self, *args, **kwargs):

        profiles = [
            {
                "email": "greg@test.com",
                "owner": {
                    "name": "Greg",
                    "age": 28,
                    "city": "London",
                    "occupation": "Photographer",
                    "about_me": (
                        "Dog dad, coffee lover, and always up for a park "
                        "playdate. Looking to meet friendly pups (and humans)."
                    ),
                    "interests": "Hiking,Coffee,Photography",
                    "profile_photo": "seed/owner_1.jpg",
                },
                "dog": {
                    "name": "Milo",
                    "age": 2,
                    "breed": "Chow Chow",
                    "energy_level": "playful",
                    "size": "medium",
                    "about_me": (
                        "Playful, cuddly, and always down for a walk. "
                        "Loves naps, treats, and making new dog friends."
                    ),
                    "profile_photo": "seed/dog_1.jpg",
                }
            },
            {
                "email": "caroline@test.com",
                "owner": {
                    "name": "Caroline",
                    "age": 31,
                    "city": "London",
                    "occupation": "Software Developer",
                    "about_me": (
                        "More coffee than tea, more walks than nightclubs."
                    ),
                    "interests": "Boxing,Surfing,Video Games",
                    "profile_photo": "seed/owner_2.jpg",
                },
                "dog": {
                    "name": "Patoo",
                    "age": 6,
                    "breed": "Finnish Lapphund",
                    "energy_level": "full zoomies",
                    "size": "medium",
                    "about_me": (
                        (
                            "I love chasing leaves and will savagely "
                            "lick your face."
                        )
                    ),
                    "profile_photo": "seed/dog_2.jpg",
                }
            },
            {
                "email": "leo@test.com",
                "owner": {
                    "name": "Leo",
                    "age": 26,
                    "city": "London",
                    "occupation": "Web Developer",
                    "about_me": (
                        "I like simple people, long talks, and happy dogs."
                    ),
                    "interests": "Cooking,Trying new restaurants,Wine",
                    "profile_photo": "seed/owner_3.jpg",
                },
                "dog": {
                    "name": "Luna",
                    "age": 3,
                    "breed": "Goldendoodle",
                    "energy_level": "chill vibes",
                    "size": "medium",
                    "about_me": (
                        "Very social, especially with humans who have treats."
                    ),
                    "profile_photo": "seed/dog_3.jpg",
                }
            },
            {
                "email": "maxg@test.com",
                "owner": {
                    "name": "Max",
                    "age": 34,
                    "city": "London",
                    "occupation": "Graphic Designer",
                    "about_me": (
                        "Looking for someone to laugh with (a lot)."
                    ),
                    "interests": "Running,Music,Podcasts",
                    "profile_photo": "seed/owner_4.jpg",
                },
                "dog": {
                    "name": "Oscar",
                    "age": 4,
                    "breed": "Border Collie",
                    "energy_level": "full zoomies",
                    "size": "large",
                    "about_me": (
                        "A bit crazy, but full of love."
                    ),
                    "profile_photo": "seed/dog_4.jpg",
                }
            },
            {
                "email": "hugo@test.com",
                "owner": {
                    "name": "Hugo",
                    "age": 32,
                    "city": "London",
                    "occupation": "Physiotherapist",
                    "about_me": (
                        "Food lover with a weakness for bad jokes."
                    ),
                    "interests": "Travel,Culture,Languages",
                    "profile_photo": "seed/owner_5.jpg",
                },
                "dog": {
                    "name": "Tilly",
                    "age": 5,
                    "breed": "Siberian Husky",
                    "energy_level": "energetic",
                    "size": "large",
                    "about_me": (
                        "Calm at home, excited the second the leash comes out."
                    ),
                    "profile_photo": "seed/dog_5.jpg",
                }
            },
            {
                "email": "martin@test.com",
                "owner": {
                    "name": "Martin",
                    "age": 36,
                    "city": "London",
                    "occupation": "Project Manager",
                    "about_me": (
                        "“Gym in the morning, Netflix at night balance."
                    ),
                    "interests": "Cinema,TV series,Writing",
                    "profile_photo": "seed/owner_6.jpg",
                },
                "dog": {
                    "name": "Simba",
                    "age": 7,
                    "breed": "Golden Retriever",
                    "energy_level": "couch potato",
                    "size": "large",
                    "about_me": (
                        "Professional cuddler with irresistible puppy eyes."
                    ),
                    "profile_photo": "seed/dog_6.jpg",
                }
            },
            {
                "email": "lea@test.com",
                "owner": {
                    "name": "Lea",
                    "age": 27,
                    "city": "London",
                    "occupation": "UX/UI Designer",
                    "about_me": (
                        "Always up for a new adventure, even a small one."
                    ),
                    "interests": "Surfing,Ocean,Sunshine",
                    "profile_photo": "seed/owner_7.jpg",
                },
                "dog": {
                    "name": "Finn",
                    "age": 3,
                    "breed": "Alaskan Malamute",
                    "energy_level": "playful",
                    "size": "medium",
                    "about_me": (
                        "Long walks and muddy puddles are my thing."
                    ),
                    "profile_photo": "seed/dog_7.jpg",
                }
            },
            {
                "email": "anna@test.com",
                "owner": {
                    "name": "Anna",
                    "age": 29,
                    "city": "London",
                    "occupation": "Yoga Instructor",
                    "about_me": (
                        "Curious, calm, and occasionally a bit awkward."
                    ),
                    "interests": "Yoga,Wellness,Meditation",
                    "profile_photo": "seed/owner_8.jpg",
                },
                "dog": {
                    "name": "Romeo",
                    "age": 2,
                    "breed": "Samoyed",
                    "energy_level": "chill vibes",
                    "size": "medium",
                    "about_me": (
                        "Always ready to play, never tired."
                    ),
                    "profile_photo": "seed/dog_8.jpg",
                }
            },
            {
                "email": "luisa@test.com",
                "owner": {
                    "name": "Luisa",
                    "age": 34,
                    "city": "London",
                    "occupation": "Consultant",
                    "about_me": (
                        "I take life seriously… but not too seriously."
                    ),
                    "interests": "Fitness,Nutrition,Health",
                    "profile_photo": "seed/owner_9.jpg",
                },
                "dog": {
                    "name": "Lola",
                    "age": 4,
                    "breed": "Cockapoo",
                    "energy_level": "couch potato",
                    "size": "medium",
                    "about_me": (
                        "Loyal, curious, and extremely food-motivated."
                    ),
                    "profile_photo": "seed/dog_9.jpg",
                }
            },
            {
                "email": "laura@test.com",
                "owner": {
                    "name": "Laura",
                    "age": 24,
                    "city": "London",
                    "occupation": "Barista",
                    "about_me": (
                        "Weekend nature trips and spontaneous brunches."
                    ),
                    "interests": "Reading,Art,Museums",
                    "profile_photo": "seed/owner_10.jpg",
                },
                "dog": {
                    "name": "Florence",
                    "age": 3,
                    "breed": "Corgi",
                    "energy_level": "couch potato",
                    "size": "small",
                    "about_me": (
                        "Small body, big personality."
                    ),
                    "profile_photo": "seed/dog_10.jpg",
                }
            },
        ]

        for data in profiles:
            user, _ = User.objects.get_or_create(
                username=data["email"],
                defaults={"email": data["email"], "password": "test1234"}
            )

            owner, _ = OwnerProfile.objects.get_or_create(
                user=user,
                defaults=data["owner"]
            )

            Dog.objects.get_or_create(
                owner=owner,
                defaults=data["dog"]
            )

        self.stdout.write(self.style.SUCCESS("Fake profiles created 🎉"))
