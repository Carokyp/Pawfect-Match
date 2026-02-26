from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import OwnerProfile


class OwnerProfileTestCase(TestCase):
    """Test OwnerProfile model CRUD operations"""
    
    def setUp(self):
        """Create a test user"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
    
    def test_owner_profile_creation(self):
        """Test creating an OwnerProfile"""
        profile = OwnerProfile.objects.create(
            user=self.user,
            name="John Doe",
            age=30,
            city="New York",
            occupation="Software Engineer",
            about_me="I love dogs!"
        )
        self.assertEqual(profile.name, "John Doe")
        self.assertEqual(profile.age, 30)
        self.assertEqual(profile.city, "New York")
        print("✓ Owner Profile Creation Test Passed")
    
    def test_owner_profile_retrieval(self):
        """Test retrieving an OwnerProfile"""
        OwnerProfile.objects.create(
            user=self.user,
            name="Jane Smith",
            age=25
        )
        retrieved = OwnerProfile.objects.get(user=self.user)
        self.assertEqual(retrieved.name, "Jane Smith")
        print("✓ Owner Profile Retrieval Test Passed")
    
    def test_owner_profile_update(self):
        """Test updating an OwnerProfile"""
        profile = OwnerProfile.objects.create(
            user=self.user,
            name="Original Name",
            age=20
        )
        profile.age = 25
        profile.save()
        updated = OwnerProfile.objects.get(user=self.user)
        self.assertEqual(updated.age, 25)
        print("✓ Owner Profile Update Test Passed")
    
    def test_owner_profile_deletion(self):
        """Test deleting an OwnerProfile"""
        profile = OwnerProfile.objects.create(
            user=self.user,
            name="To Delete"
        )
        profile.delete()
        with self.assertRaises(OwnerProfile.DoesNotExist):
            OwnerProfile.objects.get(user=self.user)
        print("✓ Owner Profile Deletion Test Passed")
    
    def test_owner_profile_str(self):
        """Test string representation"""
        profile = OwnerProfile.objects.create(
            user=self.user,
            name="Test User"
        )
        self.assertEqual(str(profile), "Test User (test@example.com)")
        print("✓ Owner Profile String Representation Test Passed")
