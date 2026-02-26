from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import OwnerProfile
from dogs.models import Dog


class DogTestCase(TestCase):
    """Test Dog model CRUD operations"""
    
    def setUp(self):
        """Create a test user and owner profile"""
        self.user = User.objects.create_user(
            username="dogowner",
            email="owner@example.com",
            password="testpass123"
        )
        self.owner_profile = OwnerProfile.objects.create(
            user=self.user,
            name="Dog Owner"
        )
    
    def test_dog_creation(self):
        """Test creating a Dog profile"""
        dog = Dog.objects.create(
            owner=self.owner_profile,
            name="Buddy",
            breed="Golden Retriever",
            age=3,
            size="large",
            gender="male",
            energy_level="energetic"
        )
        self.assertEqual(dog.name, "Buddy")
        self.assertEqual(dog.breed, "Golden Retriever")
        self.assertEqual(dog.age, 3)
        print("✓ Dog Creation Test Passed")
    
    def test_dog_retrieval(self):
        """Test retrieving a Dog profile"""
        Dog.objects.create(
            owner=self.owner_profile,
            name="Max",
            breed="Labrador"
        )
        retrieved = Dog.objects.get(name="Max")
        self.assertEqual(retrieved.breed, "Labrador")
        print("✓ Dog Retrieval Test Passed")
    
    def test_dog_update(self):
        """Test updating a Dog profile"""
        dog = Dog.objects.create(
            owner=self.owner_profile,
            name="Charlie",
            age=2
        )
        dog.age = 4
        dog.save()
        updated = Dog.objects.get(name="Charlie")
        self.assertEqual(updated.age, 4)
        print("✓ Dog Update Test Passed")
    
    def test_dog_deletion(self):
        """Test deleting a Dog profile"""
        dog = Dog.objects.create(
            owner=self.owner_profile,
            name="To Delete"
        )
        dog.delete()
        with self.assertRaises(Dog.DoesNotExist):
            Dog.objects.get(name="To Delete")
        print("✓ Dog Deletion Test Passed")
    
    def test_dog_str(self):
        """Test string representation"""
        dog = Dog.objects.create(
            owner=self.owner_profile,
            name="Bella",
            breed="Beagle"
        )
        self.assertEqual(str(dog), "Bella (Dog Owner)")
        print("✓ Dog String Representation Test Passed")
    
    def test_dog_size_choices(self):
        """Test dog size field choices"""
        dog = Dog.objects.create(
            owner=self.owner_profile,
            name="Tiny",
            size="small"
        )
        self.assertEqual(dog.get_size_display(), "Small")
        print("✓ Dog Size Choices Test Passed")
