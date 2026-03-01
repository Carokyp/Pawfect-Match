"""
Create fake owner and dog profiles for local development.

Run with: python manage.py fake_profiles
"""

import os

import cloudinary.uploader
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from dogs.models import Dog
from profiles.models import OwnerProfile


class Command(BaseCommand):
    """
    Django management command to seed fake profiles.

    Creates users, owner profiles, and dog profiles with optional
    Cloudinary uploads for seed images.
    """
    help = "fake dog & owner profiles for prototype"

    def _upload_seed_photo(self, photo_name, folder, media_seeds_path):
        """
        Upload a seed photo to Cloudinary if it exists.

        Args:
            photo_name: Filename under media_seeds_path.
            folder: Cloudinary folder to upload into.
            media_seeds_path: Base path for seed images.

        Returns:
            str | None: Cloudinary public_id if uploaded, None if failed.
        """
        photo_path = os.path.join(media_seeds_path, photo_name)
        if os.path.exists(photo_path):
            self.stdout.write(f"  Uploading photo: {photo_name}")
            try:
                # Extract filename without extension for consistent public_id
                photo_name_no_ext = photo_name.rsplit(".", 1)[0]
                public_id = f"{folder}/{photo_name_no_ext}"

                upload_result = cloudinary.uploader.upload(
                    photo_path,
                    public_id=public_id,
                    overwrite=True
                )
                photo_id = upload_result.get("public_id")
                self.stdout.write("  ✓ Photo uploaded")
                return photo_id
            except Exception as exc:
                warning_msg = f"Could not upload {photo_name}: {exc}"
                self.stdout.write(self.style.WARNING(warning_msg))
        else:
            self.stdout.write(
                self.style.WARNING(f"File not found: {photo_path}")
            )
        return None

    def handle(self, *args, **kwargs):
        """
        Run the command to create or update fake profiles.

        Args:
            *args: Positional arguments passed by Django.
            **kwargs: Keyword arguments passed by Django.
        """
        User.objects.filter(username__endswith="@test.com").delete()

        media_seeds_path = os.path.join(settings.MEDIA_ROOT, "seeds")

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
                    "interests": "Hiking, Coffee, Photography",
                    "profile_photo": "owner_1.jpg",
                },
                "dog": {
                    "name": "Milo",
                    "age": 2,
                    "breed": "Chow Chow",
                    "gender": "male",
                    "energy_level": "playful",
                    "size": "medium",
                    "about_me": (
                        "Playful, cuddly, and always down for a walk."
                        "Loves naps, treats, and making new dog friends."
                    ),
                    "profile_photo": "dog_1.jpg",
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
                    "interests": "Coffee, Travel, Music",
                    "profile_photo": "owner_2.jpg",
                },
                "dog": {
                    "name": "Patoo",
                    "age": 6,
                    "breed": "Finnish Lapphund",
                    "gender": "male",
                    "energy_level": "zoomies",
                    "size": "medium",
                    "about_me": (
                        "I love chasing leaves and will savagely "
                        " lick your face."
                    ),
                    "profile_photo": "dog_2.png",
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
                    "interests": "Cooking, Foodie, Bars",
                    "profile_photo": "owner_3.jpg",
                },
                "dog": {
                    "name": "Luna",
                    "age": 3,
                    "breed": "Goldendoodle",
                    "gender": "female",
                    "energy_level": "chill",
                    "size": "medium",
                    "about_me": (
                        "Very social, especially with humans who have treats."
                    ),
                    "profile_photo": "dog_3.jpg",
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
                    "interests": "Fitness, Music, Dancing",
                    "profile_photo": "owner_4.jpg",
                },
                "dog": {
                    "name": "Oscar",
                    "age": 4,
                    "breed": "Border Collie",
                    "gender": "male",
                    "energy_level": "zoomies",
                    "size": "large",
                    "about_me": (
                        "A bit crazy, but full of love."
                    ),
                    "profile_photo": "dog_4.jpg",
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
                    "interests": "Travel, Comedie, Bars",
                    "profile_photo": "owner_5.jpg",
                },
                "dog": {
                    "name": "Tilly",
                    "age": 5,
                    "breed": "Siberian Husky",
                    "gender": "female",
                    "energy_level": "energetic",
                    "size": "large",
                    "about_me": (
                        "Calm at home, excited the second the leash comes out."
                    ),
                    "profile_photo": "dog_5.jpg",
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
                        "Gym in the morning, Netflix at night balance."
                    ),
                    "interests": "Movies, Reading, Gaming",
                    "profile_photo": "owner_6.jpg",
                },
                "dog": {
                    "name": "Simba",
                    "age": 7,
                    "breed": "Golden Retriever",
                    "gender": "male",
                    "energy_level": "couch_potato",
                    "size": "large",
                    "about_me": (
                        "Professional cuddler with irresistible puppy eyes."
                    ),
                    "profile_photo": "dog_6.jpg",
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
                    "interests": "Travel, Art, Photography",
                    "profile_photo": "owner_7.jpg",
                },
                "dog": {
                    "name": "Finn",
                    "age": 3,
                    "breed": "Alaskan Malamute",
                    "gender": "male",
                    "energy_level": "playful",
                    "size": "medium",
                    "about_me": (
                        "Long walks and muddy puddles are my thing."
                    ),
                    "profile_photo": "dog_7.jpg",
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
                    "interests": "Yoga, Fitness, Dancing",
                    "profile_photo": "owner_8.jpg",
                },
                "dog": {
                    "name": "Romeo",
                    "age": 2,
                    "breed": "Samoyed",
                    "gender": "male",
                    "energy_level": "chill",
                    "size": "medium",
                    "about_me": (
                        "Always ready to play, never tired."
                    ),
                    "profile_photo": "dog_8.jpg",
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
                    "interests": "Fitness, Foodie, Cooking",
                    "profile_photo": "owner_9.jpg",
                },
                "dog": {
                    "name": "Lola",
                    "age": 4,
                    "breed": "Cockapoo",
                    "gender": "female",
                    "energy_level": "couch_potato",
                    "size": "medium",
                    "about_me": (
                        "Loyal, curious, and extremely food-motivated."
                    ),
                    "profile_photo": "dog_9.jpg",
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
                    "interests": "Reading, Art, Comedie",
                    "profile_photo": "owner_10.jpg",
                },
                "dog": {
                    "name": "Florence",
                    "age": 3,
                    "breed": "Corgi",
                    "gender": "female",
                    "energy_level": "couch_potato",
                    "size": "small",
                    "about_me": (
                        "Small body, big personality."
                    ),
                    "profile_photo": "dog_10.jpg",
                }
            },
        ]

        for data in profiles:
            email = data["email"]
            self.stdout.write(f"Creating profile for {email}...")

            user, _ = User.objects.get_or_create(
                username=email,
                defaults={"email": email}
            )

            user.set_unusable_password()
            user.save()

            owner_data = data["owner"].copy()
            owner_photo_name = owner_data.pop("profile_photo")

            owner_photo_id = self._upload_seed_photo(
                owner_photo_name,
                "pawfect_match/owners",
                media_seeds_path,
            )

            # Add photo ID to owner_data before creating
            if owner_photo_id:
                owner_data["profile_photo"] = owner_photo_id

            owner, created = OwnerProfile.objects.get_or_create(
                user=user,
                defaults=owner_data
            )

            # Update owner data if it already existed
            if not created:
                for key, value in owner_data.items():
                    setattr(owner, key, value)
                owner.save()

            dog_data = data["dog"].copy()
            dog_photo_name = dog_data.pop("profile_photo")

            dog_photo_id = self._upload_seed_photo(
                dog_photo_name,
                "pawfect_match/dogs",
                media_seeds_path,
            )

            # Add photo ID to dog_data before creating
            if dog_photo_id:
                dog_data["profile_photo"] = dog_photo_id

            dog, created = Dog.objects.get_or_create(
                owner=owner,
                defaults=dog_data
            )

            # Update dog data if it already existed
            if not created:
                for key, value in dog_data.items():
                    setattr(dog, key, value)
                dog.save()

        self.stdout.write(self.style.SUCCESS("Fake profiles created 🎉"))
