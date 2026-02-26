from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import OwnerProfile
from .forms import RegisterForm, LoginForm, ForgotPasswordForm


class RegisterFormTestCase(TestCase):
    """Test RegisterForm validation."""
    
    def test_registration_valid_form(self):
        """Test valid registration form with proper email and password."""
        form_data = {
            'email': 'testuser@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_registration_invalid_email(self):
        """Test registration form with invalid email format."""
        form_data = {
            'email': 'invalid_email',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_registration_passwords_dont_match(self):
        """Test registration form with mismatched passwords."""
        form_data = {
            'email': 'testuser@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'DifferentPass123!'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_registration_weak_password_no_uppercase(self):
        """Test registration form with password missing uppercase letter."""
        form_data = {
            'email': 'testuser@example.com',
            'password': 'weakpass123!',
            'password_confirm': 'weakpass123!'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_registration_weak_password_no_number(self):
        """Test registration form with password missing number."""
        form_data = {
            'email': 'testuser@example.com',
            'password': 'WeakPass!',
            'password_confirm': 'WeakPass!'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_registration_weak_password_no_special_char(self):
        """Test registration form with password missing special character."""
        form_data = {
            'email': 'testuser@example.com',
            'password': 'WeakPass123',
            'password_confirm': 'WeakPass123'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_registration_missing_email(self):
        """Test registration form with missing email."""
        form_data = {
            'email': '',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_registration_missing_password(self):
        """Test registration form with missing password."""
        form_data = {
            'email': 'testuser@example.com',
            'password': '',
            'password_confirm': ''
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())


class LoginFormTestCase(TestCase):
    """Test LoginForm validation."""
    
    def setUp(self):
        """Create a test user for login tests."""
        User.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='SecurePass123!'
        )
    
    def test_login_form_valid_credentials(self):
        """Test login form with valid credentials."""
        form_data = {
            'username': 'testuser@example.com',
            'password': 'SecurePass123!'
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_login_form_invalid_password(self):
        """Test login form with incorrect password."""
        form_data = {
            'username': 'testuser@example.com',
            'password': 'WrongPassword123!'
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_login_form_nonexistent_user(self):
        """Test login form with non-existent user."""
        form_data = {
            'username': 'nonexistent@example.com',
            'password': 'SecurePass123!'
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_login_form_missing_username(self):
        """Test login form with missing username."""
        form_data = {
            'username': '',
            'password': 'SecurePass123!'
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_login_form_missing_password(self):
        """Test login form with missing password."""
        form_data = {
            'username': 'testuser@example.com',
            'password': ''
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())


class ForgotPasswordFormTestCase(TestCase):
    """Test ForgotPasswordForm validation."""
    
    def setUp(self):
        """Create a test user for password reset tests."""
        self.user = User.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='OldPass123!'
        )
        OwnerProfile.objects.create(
            user=self.user,
            name='Test User',
            age=30,
            city='Test City'
        )
    
    def test_forgot_password_valid_form(self):
        """Test forgot password form with valid email and matching passwords."""
        form_data = {
            'email': 'testuser@example.com',
            'new_password': 'NewPass123!',
            'new_password_confirm': 'NewPass123!'
        }
        form = ForgotPasswordForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_forgot_password_nonexistent_email(self):
        """Test forgot password form with non-existent email."""
        form_data = {
            'email': 'nonexistent@example.com',
            'new_password': 'NewPass123!',
            'new_password_confirm': 'NewPass123!'
        }
        form = ForgotPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_forgot_password_mismatched_passwords(self):
        """Test forgot password form with mismatched new passwords."""
        form_data = {
            'email': 'testuser@example.com',
            'new_password': 'NewPass123!',
            'new_password_confirm': 'DifferentPass123!'
        }
        form = ForgotPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_forgot_password_weak_password(self):
        """Test forgot password form with weak password."""
        form_data = {
            'email': 'testuser@example.com',
            'new_password': 'weak',
            'new_password_confirm': 'weak'
        }
        form = ForgotPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_forgot_password_no_special_character(self):
        """Test forgot password form with password missing special character."""
        form_data = {
            'email': 'testuser@example.com',
            'new_password': 'NewPass123',
            'new_password_confirm': 'NewPass123'
        }
        form = ForgotPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_forgot_password_no_uppercase(self):
        """Test forgot password form with password missing uppercase."""
        form_data = {
            'email': 'testuser@example.com',
            'new_password': 'newpass123!',
            'new_password_confirm': 'newpass123!'
        }
        form = ForgotPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_forgot_password_no_digit(self):
        """Test forgot password form with password missing digit."""
        form_data = {
            'email': 'testuser@example.com',
            'new_password': 'NewPass!',
            'new_password_confirm': 'NewPass!'
        }
        form = ForgotPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserAuthenticationTestCase(TestCase):
    """Test user authentication workflows."""
    
    def setUp(self):
        """Create a test user."""
        self.user = User.objects.create_user(
            username='authtest@example.com',
            email='authtest@example.com',
            password='SecurePass123!'
        )
    
    def test_user_creation(self):
        """Test that user is created successfully."""
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.username, 'authtest@example.com')
    
    def test_user_password_hashed(self):
        """Test that user password is hashed, not stored as plain text."""
        stored_user = User.objects.get(username='authtest@example.com')
        self.assertNotEqual(stored_user.password, 'SecurePass123!')
        self.assertTrue(stored_user.check_password('SecurePass123!'))
    
    def test_user_authentication_correct_password(self):
        """Test user authentication with correct password."""
        auth_user = self.client.login(
            username='authtest@example.com',
            password='SecurePass123!'
        )
        self.assertTrue(auth_user)
    
    def test_user_authentication_incorrect_password(self):
        """Test user authentication fails with incorrect password."""
        auth_user = self.client.login(
            username='authtest@example.com',
            password='WrongPassword123!'
        )
        self.assertFalse(auth_user)
    
    def test_user_password_change(self):
        """Test user password can be changed."""
        self.user.set_password('NewSecurePass123!')
        self.user.save()
        
        # Old password should not work
        self.assertFalse(self.user.check_password('SecurePass123!'))
        # New password should work
        self.assertTrue(self.user.check_password('NewSecurePass123!'))
