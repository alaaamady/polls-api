from django.test import TestCase, Client
from .models import Choice, Vote
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Poll, Choice, Vote
from rest_framework.test import APIRequestFactory
from .views import VoteViewSet
from django.core import mail


"""
VIEWS TEST
"""


###### POLL ######

class PollViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.poll1 = Poll.objects.create(
            title='Test Poll 1', description='Description 1')
        self.poll2 = Poll.objects.create(
            title='Test Poll 2', description='Description 2')

    def test_retrieve_list_of_polls(self):
        response = self.client.get('/polls/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_retrieve_single_poll(self):
        response = self.client.get('/polls/{}/'.format(self.poll1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Poll 1')

    def test_create_poll(self):
        data = {
            'title': 'Test Poll 3',
            'description': 'Description 3'
        }
        response = self.client.post('/polls/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Poll.objects.count(), 3)

    def test_update_poll(self):
        data = {
            'title': 'Test Poll 1 Updated',
            'description': 'Description 1 Updated'
        }
        response = self.client.put('/polls/{}/'.format(self.poll1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Poll 1 Updated')

    def test_delete_poll(self):
        response = self.client.delete('/polls/{}/'.format(self.poll1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Poll.objects.count(), 1)

    def test_search_filter(self):
        response = self.client.get('/polls/', {'search': 'Test Poll 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Poll 1')

##### VOTE #####


class VoteViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = VoteViewSet.as_view({'post': 'create'})
        self.client = Client()

        self.poll = Poll.objects.create(
            title='Test Poll', description='Test Description')
        self.choice = Choice.objects.create(text='Test Choice', poll=self.poll)
        self.valid_payload = {
            'poll_id': self.poll.id,
            'choice_id': self.choice.id,
            'email': 'test@example.com'
        }
        self.invalid_payload = {
            'poll_id': 999,
            'choice_id': 999,
            'email': 'test@example.com'
        }

    def test_create_vote(self):
        request = self.factory.post('/vote/', self.valid_payload)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vote.objects.count(), 1)

    def test_create_vote_with_invalid_choice_id(self):
        request = self.factory.post('/vote/', self.invalid_payload)
        response = self.view(request)
        print(response.data['choice_id'][0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['choice_id']
                         [0], 'Choice does not exist.')

    def test_send_otp_email(self):
        self.client.post('/vote/', self.valid_payload)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         'Your One-Time Password for Voting')
