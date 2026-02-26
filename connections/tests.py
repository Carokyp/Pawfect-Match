from django.test import TestCase
from django.contrib.auth.models import User
from dogs.models import Dog
from profiles.models import OwnerProfile
from .models import Connection, Dislike


class ConnectionModelTestCase(TestCase):
    """Test Connection model CRUD operations."""
    
    def setUp(self):
        """Create test users, owner profiles, and dogs."""
        # Create first user and dog
        self.user1 = User.objects.create_user(
            username='owner1@example.com',
            email='owner1@example.com',
            password='SecurePass123!'
        )
        self.owner1 = OwnerProfile.objects.create(
            user=self.user1,
            name='Owner One',
            age=30,
            city='City One',
            about_me='Love dogs!'
        )
        self.dog1 = Dog.objects.create(
            owner=self.owner1,
            name='Buddy',
            age=3,
            size='medium',
            gender='male',
            about_me='Friendly and playful'
        )
        
        # Create second user and dog
        self.user2 = User.objects.create_user(
            username='owner2@example.com',
            email='owner2@example.com',
            password='SecurePass123!'
        )
        self.owner2 = OwnerProfile.objects.create(
            user=self.user2,
            name='Owner Two',
            age=28,
            city='City Two',
            about_me='Dog lover'
        )
        self.dog2 = Dog.objects.create(
            owner=self.owner2,
            name='Luna',
            age=2,
            size='small',
            gender='female',
            about_me='Sweet and gentle'
        )
    
    def test_connection_creation(self):
        """Test that a connection can be created between two dogs."""
        connection = Connection.objects.create(
            from_dog=self.dog1,
            to_dog=self.dog2
        )
        self.assertEqual(connection.from_dog, self.dog1)
        self.assertEqual(connection.to_dog, self.dog2)
        self.assertEqual(Connection.objects.count(), 1)
    
    def test_connection_retrieval(self):
        """Test retrieving a connection."""
        connection = Connection.objects.create(
            from_dog=self.dog1,
            to_dog=self.dog2
        )
        retrieved_connection = Connection.objects.get(
            from_dog=self.dog1,
            to_dog=self.dog2
        )
        self.assertEqual(retrieved_connection.id, connection.id)
        self.assertEqual(retrieved_connection.from_dog.name, 'Buddy')
        self.assertEqual(retrieved_connection.to_dog.name, 'Luna')
    
    def test_connection_timestamp(self):
        """Test that connection has a creation timestamp."""
        connection = Connection.objects.create(
            from_dog=self.dog1,
            to_dog=self.dog2
        )
        self.assertIsNotNone(connection.created_at)
    
    def test_connection_string_representation(self):
        """Test connection string representation."""
        connection = Connection.objects.create(
            from_dog=self.dog1,
            to_dog=self.dog2
        )
        # Connection __str__ includes owner names from Dog's __str__ method
        expected_str = "Buddy (Owner One) ❤️ Luna (Owner Two)"
        self.assertEqual(str(connection), expected_str)
    
    def test_multiple_connections(self):
        """Test creating multiple connections."""
        # Create third dog
        self.user3 = User.objects.create_user(
            username='owner3@example.com',
            email='owner3@example.com',
            password='SecurePass123!'
        )
        self.owner3 = OwnerProfile.objects.create(
            user=self.user3,
            name='Owner Three',
            age=25,
            city='City Three',
            about_me='Dog enthusiast'
        )
        self.dog3 = Dog.objects.create(
            owner=self.owner3,
            name='Charlie',
            age=4,
            size='large',
            gender='male',
            about_me='Energetic and loyal'
        )
        
        # Create multiple connections
        Connection.objects.create(from_dog=self.dog1, to_dog=self.dog2)
        Connection.objects.create(from_dog=self.dog1, to_dog=self.dog3)
        Connection.objects.create(from_dog=self.dog2, to_dog=self.dog3)
        
        self.assertEqual(Connection.objects.count(), 3)
    
    def test_connection_relationships(self):
        """Test connection relationships with related names."""
        Connection.objects.create(from_dog=self.dog1, to_dog=self.dog2)
        Connection.objects.create(from_dog=self.dog2, to_dog=self.dog1)
        
        # Test sent_connections
        sent = self.dog1.sent_connections.all()
        self.assertEqual(sent.count(), 1)
        self.assertEqual(sent.first().to_dog, self.dog2)
        
        # Test received_connections
        received = self.dog1.received_connections.all()
        self.assertEqual(received.count(), 1)
        self.assertEqual(received.first().from_dog, self.dog2)
    
    def test_connection_deletion(self):
        """Test that connection can be deleted."""
        connection = Connection.objects.create(
            from_dog=self.dog1,
            to_dog=self.dog2
        )
        self.assertEqual(Connection.objects.count(), 1)
        
        connection.delete()
        self.assertEqual(Connection.objects.count(), 0)
    
    def test_connection_cascade_delete(self):
        """Test that connections are deleted when a dog is deleted."""
        Connection.objects.create(from_dog=self.dog1, to_dog=self.dog2)
        Connection.objects.create(from_dog=self.dog2, to_dog=self.dog1)
        
        self.assertEqual(Connection.objects.count(), 2)
        
        # Delete dog1
        self.dog1.delete()
        
        # All connections involving dog1 should be deleted
        self.assertEqual(Connection.objects.count(), 0)


class DislikeModelTestCase(TestCase):
    """Test Dislike model CRUD operations."""
    
    def setUp(self):
        """Create test users, owner profiles, and dogs."""
        # Create first user and dog
        self.user1 = User.objects.create_user(
            username='owner1@example.com',
            email='owner1@example.com',
            password='SecurePass123!'
        )
        self.owner1 = OwnerProfile.objects.create(
            user=self.user1,
            name='Owner One',
            age=30,
            city='City One',
            about_me='Love dogs!'
        )
        self.dog1 = Dog.objects.create(
            owner=self.owner1,
            name='Buddy',
            age=3,
            size='medium',
            gender='male',
            about_me='Friendly and playful'
        )
        
        # Create second user and dog
        self.user2 = User.objects.create_user(
            username='owner2@example.com',
            email='owner2@example.com',
            password='SecurePass123!'
        )
        self.owner2 = OwnerProfile.objects.create(
            user=self.user2,
            name='Owner Two',
            age=28,
            city='City Two',
            about_me='Dog lover'
        )
        self.dog2 = Dog.objects.create(
            owner=self.owner2,
            name='Luna',
            age=2,
            size='small',
            gender='female',
            about_me='Sweet and gentle'
        )
    
    def test_dislike_creation(self):
        """Test that a dislike can be created between two dogs."""
        dislike = Dislike.objects.create(
            from_dog=self.dog1,
            to_dog=self.dog2
        )
        self.assertEqual(dislike.from_dog, self.dog1)
        self.assertEqual(dislike.to_dog, self.dog2)
        self.assertEqual(Dislike.objects.count(), 1)
    
    def test_dislike_retrieval(self):
        """Test retrieving a dislike."""
        dislike = Dislike.objects.create(
            from_dog=self.dog1,
            to_dog=self.dog2
        )
        retrieved_dislike = Dislike.objects.get(
            from_dog=self.dog1,
            to_dog=self.dog2
        )
        self.assertEqual(retrieved_dislike.id, dislike.id)
    
    def test_dislike_timestamp(self):
        """Test that dislike has a creation timestamp."""
        dislike = Dislike.objects.create(
            from_dog=self.dog1,
            to_dog=self.dog2
        )
        self.assertIsNotNone(dislike.created_at)
    
    def test_multiple_dislikes(self):
        """Test creating multiple dislikes."""
        # Create third dog
        self.user3 = User.objects.create_user(
            username='owner3@example.com',
            email='owner3@example.com',
            password='SecurePass123!'
        )
        self.owner3 = OwnerProfile.objects.create(
            user=self.user3,
            name='Owner Three',
            age=25,
            city='City Three',
            about_me='Dog enthusiast'
        )
        self.dog3 = Dog.objects.create(
            owner=self.owner3,
            name='Charlie',
            age=4,
            size='large',
            gender='male',
            about_me='Energetic and loyal'
        )
        
        # Create multiple dislikes
        Dislike.objects.create(from_dog=self.dog1, to_dog=self.dog2)
        Dislike.objects.create(from_dog=self.dog1, to_dog=self.dog3)
        Dislike.objects.create(from_dog=self.dog2, to_dog=self.dog3)
        
        self.assertEqual(Dislike.objects.count(), 3)
    
    def test_dislike_relationships(self):
        """Test dislike relationships with related names."""
        Dislike.objects.create(from_dog=self.dog1, to_dog=self.dog2)
        Dislike.objects.create(from_dog=self.dog2, to_dog=self.dog1)
        
        # Test dislikes_given
        given = self.dog1.dislikes_given.all()
        self.assertEqual(given.count(), 1)
        self.assertEqual(given.first().to_dog, self.dog2)
        
        # Test dislikes_received
        received = self.dog1.dislikes_received.all()
        self.assertEqual(received.count(), 1)
        self.assertEqual(received.first().from_dog, self.dog2)
    
    def test_dislike_deletion(self):
        """Test that dislike can be deleted."""
        dislike = Dislike.objects.create(
            from_dog=self.dog1,
            to_dog=self.dog2
        )
        self.assertEqual(Dislike.objects.count(), 1)
        
        dislike.delete()
        self.assertEqual(Dislike.objects.count(), 0)
    
    def test_dislike_cascade_delete(self):
        """Test that dislikes are deleted when a dog is deleted."""
        Dislike.objects.create(from_dog=self.dog1, to_dog=self.dog2)
        Dislike.objects.create(from_dog=self.dog2, to_dog=self.dog1)
        
        self.assertEqual(Dislike.objects.count(), 2)
        
        # Delete dog1
        self.dog1.delete()
        
        # All dislikes involving dog1 should be deleted
        self.assertEqual(Dislike.objects.count(), 0)


class ConnectionAndDislikeSeparationTestCase(TestCase):
    """Test that connections and dislikes work independently."""
    
    def setUp(self):
        """Create test data."""
        self.user1 = User.objects.create_user(
            username='owner1@example.com',
            email='owner1@example.com',
            password='SecurePass123!'
        )
        self.owner1 = OwnerProfile.objects.create(
            user=self.user1,
            name='Owner One',
            age=30,
            city='City One',
            about_me='Love dogs!'
        )
        self.dog1 = Dog.objects.create(
            owner=self.owner1,
            name='Buddy',
            age=3,
            size='medium',
            gender='male',
            about_me='Friendly and playful'
        )
        
        self.user2 = User.objects.create_user(
            username='owner2@example.com',
            email='owner2@example.com',
            password='SecurePass123!'
        )
        self.owner2 = OwnerProfile.objects.create(
            user=self.user2,
            name='Owner Two',
            age=28,
            city='City Two',
            about_me='Dog lover'
        )
        self.dog2 = Dog.objects.create(
            owner=self.owner2,
            name='Luna',
            age=2,
            size='small',
            gender='female',
            about_me='Sweet and gentle'
        )
    
    def test_connection_and_dislike_coexist(self):
        """Test that connection and dislike can coexist for same dog pair."""
        # Create both connection and dislike
        Connection.objects.create(
            from_dog=self.dog1,
            to_dog=self.dog2
        )
        Dislike.objects.create(
            from_dog=self.dog1,
            to_dog=self.dog2
        )
        
        self.assertEqual(Connection.objects.count(), 1)
        self.assertEqual(Dislike.objects.count(), 1)
    
    def test_separate_dislike_connections(self):
        """Test that creating dislike doesn't affect connections."""
        Connection.objects.create(from_dog=self.dog1, to_dog=self.dog2)
        initial_connections = Connection.objects.count()
        
        Dislike.objects.create(from_dog=self.dog1, to_dog=self.dog2)
        
        self.assertEqual(Connection.objects.count(), initial_connections)

