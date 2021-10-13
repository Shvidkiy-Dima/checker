import asyncio
import time
import io
import json
import subprocess
import sys, os
from subprocess import PIPE
from rest_framework.test import APITestCase, APIClient
from multiprocessing import Process, Pipe
from background_service.fetcher.runner import start as f_start
from background_service.notifier.runner import start as n_start, \
    EmailSender, TelegramSender
from monitor.models import Monitor
from django.urls import reverse
from account.models import User
from rest_framework.authtoken.models import Token
from django.db import connections, connection
from unittest.mock import patch, AsyncMock
from functools import partial


def telegram_send(conn, *args, **kwargs):
    print('TELEGA')
    conn.send('telegram')


def email_send(conn, *args, **kwargs):
    print("EMAIL")
    conn.send('email')


class TestMonitor(APITestCase):

    processes = []

    @classmethod
    def _rollback_atomics(cls, *args, **kwargs):
        pass


    @classmethod
    def setUpTestData(cls):
        cls.rest_client = APIClient()

    @property
    def _create_monitor_url(self):
        return reverse('monitor:monitor')

    @classmethod
    def tearDownClass(cls):
        for p in cls.processes:
            p.kill()

        super().tearDownClass()


    def start_fetcher(self):

        def _start_fetcher(conn):
            # reopen in child ( use another fd)

            connection.connect()

            # drop stderr and stdout

            # sys.stderr = io.BytesIO()
            # sys.stdout = io.BytesIO()

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            conn.send(1)
            f_start()

        parent_conn, child_conn = Pipe()
        p = Process(target=_start_fetcher, args=(child_conn,))
        p.start()
        self.processes.append(p)
        parent_conn.recv()
        return parent_conn, child_conn


    def start_notifier(self, e_mock, t_mock):

        def _start_notifier(conn):
            # reopen in child ( use another fd)

            connection.connect()

            # drop stderr and stdout

            # sys.stderr = io.BytesIO()
            # sys.stdout = io.BytesIO()

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            conn.send(1)
            n_start()

        parent_conn, child_conn = Pipe()

        e_mock.side_effect = partial(email_send, child_conn)
        t_mock.side_effect = partial(telegram_send, child_conn)

        p = Process(target=_start_notifier, args=(child_conn,))
        p.start()
        self.processes.append(p)
        parent_conn.recv()

        return parent_conn, child_conn


    @patch.object(EmailSender, 'send_message', new_callable=AsyncMock)
    @patch.object(TelegramSender, 'send_message',  new_callable=AsyncMock)
    def test_monitor(self, e_mock, t_mock):

        # close connection
        connections.close_all()

        f_parent_conn, f_child_conn = self.start_notifier(e_mock, t_mock)
        self.start_fetcher()

        # reopen
        connection.connect()

        user = User.objects.make_client('test@mail.com', '123456')
        user.telegram_chat_id = '12345'
        user.save(update_fields=['telegram_chat_id'])

        token, _ = Token.objects.get_or_create(user=user)
        data = {"interval": 60,
                "error_notification_interval": 60,
                "max_timeout": 10,
                "by_telegram": True,
                "by_email": True,
                "name": "Test",
                "url": "https://www.google.com/"}

        res = self.rest_client.post(
            self._create_monitor_url,
            data=data,
            HTTP_AUTHORIZATION=f"Token {token.key}",
            format='json'
        )

        self.assertTrue(res.status_code == 201)
        self.assertTrue(Monitor.objects.count() == 1)
        monitor: Monitor = Monitor.objects.get()

        self.assertTrue(monitor.logs.count() == 1)
        print(monitor.logs.all())
        self.assertTrue(len(list(
            filter(lambda l: l.is_successful, monitor.logs.all()))) == 1)

        print('Sleep one')
        time.sleep(80)
        self.assertTrue(len(list(
            filter(lambda l: l.is_successful, monitor.logs.all()))) == 2)

        monitor.url = 'http://lala-lend.tttt'
        monitor.save(update_fields=['url'])

        print('Sleep two')
        time.sleep(80)
        self.assertTrue(len(list(
            filter(lambda l: not l.is_successful, monitor.logs.all()))) >= 1)

        telegram = False
        email = False

        print('Wait msgs')
        for _ in range(60):
            have_data = f_parent_conn.poll(1)

            if not have_data:
                continue

            data = f_parent_conn.recv()

            if data == 'telegram':
                print('Telegram ok')
                telegram = True

            elif data == 'email':
                print('Email ok')
                email = True

            if telegram and email:
                break

        if not email:
            self.assertTrue(False, 'Email error')

        if not telegram:
            self.assertTrue(False, 'Telegram error')
