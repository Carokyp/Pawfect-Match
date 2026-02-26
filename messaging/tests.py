from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import OwnerProfile
from dogs.models import Dog
from messaging.models import Message


class MessageTestCase(TestCase):
    """Test Message model CRUD operations"""
    
    def setUp(self):
        """Create two users with dogs for messaging"""
        # First user and dog
        self.user1 = User.objects.create_user(
            username="sender",
            email="sender@example.com",
            password="testpass123"
        )
        self.owner1 = OwnerProfile.objects.create(
            user=self.user1,
            name="Sender Owner"
        )
        self.dog1 = Dog.objects.create(
            owner=self.owner1,
            name="Buddy",
            breed="Golden Retriever"
        )
        
        # Second user and dog
        self.user2 = User.objects.create_user(
            username="receiver",
            email="receiver@example.com",
            password="testpass123"
        )
        self.owner2 = OwnerProfile.objects.create(
            user=self.user2,
            name="Receiver Owner"
        )
        self.dog2 = Dog.objects.create(
            owner=self.owner2,
            name="Max",
            breed="Labrador"
        )
    
    def test_message_creation(self):
        """Test creating a Message"""
        message = Message.objects.create(
            sender_dog=self.dog1,
            receiver_dog=self.dog2,
            content="Hey Max, want to play?"
        )
        self.assertEqual(message.content, "Hey Max, want to play?")
        self.assertEqual(message.sender_dog.name, "Buddy")
        print("✓ Message Creation Test Passed")
    
    def test_message_retrieval(self):
        """Test retrieving a Message"""
        message = Message.objects.create(
            sender_dog=self.dog1,
            receiver_dog=self.dog2,
            content="Test message"
        )
        self.assertIsNotNone(message)
        retrieved = Message.objects.get(content="Test message")
        self.assertEqual(retrieved.sender_dog.name, "Buddy")
        self.assertEqual(retrieved.receiver_dog.name, "Max")
        print("✓ Message Retrieval Test Passed")
    
    def test_message_update(self):
        """Test updating a Message (update content)"""
        message = Message.objects.create(
            sender_dog=self.dog1,
            receiver_dog=self.dog2,
            content="Original message"
        )
        message.content = "Updated message"
        message.save()
        updated = Message.objects.get(id=message.id)
        self.assertEqual(updated.content, "Updated message")
        print("✓ Message Update Test Passed")
    
    def test_message_deletion(self):
        """Test deleting a Message"""
        message = Message.objects.create(
            sender_dog=self.dog1,
            receiver_dog=self.dog2,
            content="To delete"
        )
        message_id = message.id
        message.delete()
        with self.assertRaises(Message.DoesNotExist):
            Message.objects.get(id=message_id)
        print("✓ Message Deletion Test Passed")
    
    def test_message_str(self):
        """Test string representation"""
        message = Message.objects.create(
            sender_dog=self.dog1,
            receiver_dog=self.dog2,
            content="Test"
        )
        self.assertEqual(str(message), "Buddy → Max")
        print("✓ Message String Representation Test Passed")
    
    def test_multiple_messages(self):
        """Test multiple messages between dogs"""
        Message.objects.create(
            sender_dog=self.dog1,
            receiver_dog=self.dog2,
            content="First message"
        )
        Message.objects.create(
            sender_dog=self.dog2,
            receiver_dog=self.dog1,
            content="Reply message"
        )
        messages = Message.objects.all()
        self.assertEqual(messages.count(), 2)
        print("✓ Multiple Messages Test Passed")
