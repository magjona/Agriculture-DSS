from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Farmer, Farm, Crop, Recommendation, Manager, ChatSession, ChatMessage

class CoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create farmer
        self.farmer = Farmer.objects.create(
            user=self.user,
            location='Kampala'
        )
        
        # Create farm
        self.farm = Farm.objects.create(
            farmer=self.farmer,
            name='Test Farm',
            size_acres=5.0,
            soil_type='loamy',
            water_source='Well'
        )
        
        # Create crop
        self.crop = Crop.objects.create(
            name='Maize',
            ideal_soil='loamy',
            planting_season='March - April',
            expected_yield_per_acre='30 bags',
            description='Ugandan maize',
            factors_favouring='Grows well in loamy soil',
            layman_knowledge='Plant early in March'
        )

    def test_farmer_creation(self):
        """Test that a Farmer object is created correctly."""
        self.assertEqual(self.farmer.user.username, 'testuser')
        self.assertEqual(self.farmer.location, 'Kampala')

    def test_farm_creation(self):
        """Test that a Farm object is created correctly."""
        self.assertEqual(self.farm.name, 'Test Farm')
        self.assertEqual(self.farm.farmer, self.farmer)
        self.assertEqual(self.farm.soil_type, 'loamy')

    def test_crop_creation(self):
        """Test that a Crop object is created correctly."""
        self.assertEqual(self.crop.name, 'Maize')
        self.assertEqual(self.crop.ideal_soil, 'loamy')
        self.assertIsNotNone(self.crop.factors_favouring)

    def test_recommendation_generation(self):
        """Test that a Recommendation can be created."""
        recommendation = Recommendation.objects.create(
            farm=self.farm,
            crop=self.crop,
            fertilizer_info='Test fertilizer info',
            pesticide_info='Test pesticide info',
            irrigation_info='Test irrigation info'
        )
        self.assertEqual(recommendation.farm, self.farm)
        self.assertEqual(recommendation.crop, self.crop)

    def test_farmer_dashboard_access(self):
        """Test that a logged-in farmer can access the dashboard."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Farm')

    def test_manager_profile_creation(self):
        """Test that a Manager profile can be created."""
        manager_user = User.objects.create_user(
            username='manager',
            password='managerpass',
            is_staff=True
        )
        manager = Manager.objects.create(
            user=manager_user,
            department='Agriculture'
        )
        self.assertEqual(manager.user.username, 'manager')

    def test_landing_page(self):
        """Test that the landing page loads correctly."""
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Farm Decision Support System')

    def test_chat_session_creation(self):
        """Test that a ChatSession can be created correctly."""
        session = ChatSession.objects.create(
            farmer=self.farmer,
            title='Test Chat Session'
        )
        self.assertEqual(session.farmer, self.farmer)
        self.assertEqual(session.title, 'Test Chat Session')

    def test_chat_message_creation(self):
        """Test that a ChatMessage can be created and linked to a session."""
        session = ChatSession.objects.create(
            farmer=self.farmer,
            title='Test Chat Session'
        )
        message = ChatMessage.objects.create(
            session=session,
            role='user',
            content='Hello Musa'
        )
        self.assertEqual(message.session, session)
        self.assertEqual(message.role, 'user')
        self.assertEqual(message.content, 'Hello Musa')

    def test_chat_index_redirects(self):
        """Test that a logged-in farmer accessing /chat/ gets redirected."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('chat_index'))
        # Should redirect to the active or newly created chat session
        self.assertEqual(response.status_code, 302)

    def test_chat_session_view(self):
        """Test that the chat session page loads successfully."""
        self.client.login(username='testuser', password='testpass123')
        session = ChatSession.objects.create(
            farmer=self.farmer,
            title='Advisory Chat'
        )
        response = self.client.get(reverse('chat_session', args=[session.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Advisory Chat')
        self.assertContains(response, 'Musa - FarmDSS AI Advisor')
