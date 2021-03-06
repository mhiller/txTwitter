from twisted.trial.unittest import TestCase


class TestTweetFunctions(TestCase):
    def setUp(self):
        from txtwitter import messagetools
        self.messagetools = messagetools

    def test_is_tweet(self):
        """
        is_tweet() should return `True` for a tweet message.
        """
        self.assertEqual(True, self.messagetools.is_tweet({
            'id_str': '12345',
            'text': 'This is a tweet.',
            'user': {},
        }))

    def test_is_tweet_nontweet(self):
        """
        is_tweet() should return `False` for a non-tweet message.
        """
        self.assertEqual(False, self.messagetools.is_tweet({
            'friends': [],
        }))

    def test_ensure_tweet(self):
        """
        ensure_tweet() should return the original message for a tweet message.
        """
        msg = {
            'id_str': '12345',
            'text': 'This is a tweet.',
            'user': {},
        }
        self.assertEqual(msg, self.messagetools.ensure_tweet(msg))

    def test_ensure_tweet_nontweet(self):
        """
        ensure_tweet() should rase `ValueError` for a non-tweet message.
        """
        msg = {'friends': []}
        self.assertRaises(ValueError, self.messagetools.ensure_tweet, msg)

    def test_tweet_id(self):
        """
        tweet_id() should return the `id_str` field of a tweet message.
        """
        msg = {
            'id_str': '12345',
            'text': 'This is a tweet.',
            'user': {},
        }
        self.assertEqual('12345', self.messagetools.tweet_id(msg))

    def test_tweet_id_nontweet(self):
        """
        tweet_id() should rase `ValueError` for a non-tweet message.
        """
        msg = {'friends': []}
        self.assertRaises(ValueError, self.messagetools.tweet_id, msg)

    def test_tweet_text(self):
        """
        tweet_text() should return the `text` field of a tweet message.
        """
        msg = {
            'id_str': '12345',
            'text': 'This is a tweet.',
            'user': {},
        }
        self.assertEqual('This is a tweet.', self.messagetools.tweet_text(msg))

    def test_tweet_text_nontweet(self):
        """
        tweet_text() should rase `ValueError` for a non-tweet message.
        """
        msg = {'friends': []}
        self.assertRaises(ValueError, self.messagetools.tweet_text, msg)

    def test_tweet_user_mentions(self):
        """
        tweet_user_mentions() should return the list of users mentioned in the
        tweet message.
        """
        user_mention = {
            'id_str': '123',
            'screen_name': 'fakeuser',
            'name': 'Fake User',
        }
        msg = {
            'entities': {'user_mentions': [user_mention]},
            'id_str': '12345',
            'text': 'This is a tweet mentioning @fakeuser.',
            'user': {},
        }
        self.assertEqual(
            [user_mention], self.messagetools.tweet_user_mentions(msg))

    def test_tweet_user_mentions_no_mentions(self):
        """
        tweet_user_mentions() should return an empty list if no users are
        mentioned in the tweet message.
        """
        msg = {
            'entities': {'user_mentions': []},
            'id_str': '12345',
            'text': 'This is a tweet mentioning @fakeuser.',
            'user': {},
        }
        self.assertEqual([], self.messagetools.tweet_user_mentions(msg))

    def test_tweet_user_mentions_nontweet(self):
        """
        tweet_user_mentions() should rase `ValueError` for a non-tweet message.
        """
        msg = {'friends': []}
        self.assertRaises(
            ValueError, self.messagetools.tweet_user_mentions, msg)

    def test_tweet_in_reply_to_id(self):
        """
        tweet_in_reply_to_id() should return the id of the tweet this tweet
        message is a reply to.
        """
        msg = {
            'id_str': '12345',
            'in_reply_to_status_id_str': '12344',
            'text': '@fakeuser This is a reply.',
            'user': {},
        }
        self.assertEqual('12344', self.messagetools.tweet_in_reply_to_id(msg))

    def test_tweet_in_reply_to_id_nonreply(self):
        """
        tweet_in_reply_to_id() should return `None` if this tweet message is
        not a reply.
        """
        msg = {
            'id_str': '12345',
            'in_reply_to_status_id_str': None,
            'text': '@fakeuser This is a reply.',
            'user': {},
        }
        self.assertEqual(None, self.messagetools.tweet_in_reply_to_id(msg))

    def test_tweet_in_reply_to_id_nontweet(self):
        """
        tweet_in_reply_to_id() should rase `ValueError` for a non-tweet
        message.
        """
        msg = {'friends': []}
        self.assertRaises(
            ValueError, self.messagetools.tweet_in_reply_to_id, msg)

    def test_tweet_in_reply_to_screen_name(self):
        """
        tweet_in_reply_to_screen_name() should return the screen name of the
        user who's tweet this tweet message is a reply to.
        """
        msg = {
            'id_str': '12345',
            'in_reply_to_status_id_str': '12344',
            'in_reply_to_screen_name': 'sam',
            'text': '@fakeuser This is a reply.',
            'user': {},
        }
        self.assertEqual(
            'sam', self.messagetools.tweet_in_reply_to_screen_name(msg))

    def test_tweet_in_reply_to_screen_name_nonreply(self):
        """
        tweet_in_reply_to_screen_name() should return `None` if this tweet
        message is not a reply.
        """
        msg = {
            'id_str': '12345',
            'in_reply_to_status_id_str': None,
            'in_reply_to_screen_name': None,
            'text': '@fakeuser This is a reply.',
            'user': {},
        }
        self.assertEqual(
            None, self.messagetools.tweet_in_reply_to_screen_name(msg))

    def test_tweet_in_reply_to_screen_name_nontweet(self):
        """
        tweet_in_reply_to_screen_name() should rase `ValueError` for a
        non-tweet message.
        """
        msg = {'friends': []}
        self.assertRaises(
            ValueError, self.messagetools.tweet_in_reply_to_screen_name, msg)

    def test_tweet_is_reply(self):
        """
        tweet_in_reply_to_id() should return `True` if this tweet message is a
        reply.
        """
        msg = {
            'id_str': '12345',
            'in_reply_to_status_id_str': '12344',
            'text': '@fakeuser This is a reply.',
            'user': {},
        }
        self.assertEqual(True, self.messagetools.tweet_is_reply(msg))

    def test_tweet_is_reply_nonreply(self):
        """
        tweet_is_reply() should return `False` if this tweet message is not a
        reply.
        """
        msg = {
            'id_str': '12345',
            'in_reply_to_status_id_str': None,
            'text': '@fakeuser This is a reply.',
            'user': {},
        }
        self.assertEqual(False, self.messagetools.tweet_is_reply(msg))

    def test_tweet_is_reply_nontweet(self):
        """
        tweet_is_reply() should rase `ValueError` for a non-tweet message.
        """
        msg = {'friends': []}
        self.assertRaises(ValueError, self.messagetools.tweet_is_reply, msg)

    def test_tweet_user(self):
        """
        tweet_user() should return the `user` field of a tweet message.
        """
        msg = {
            'id_str': '12345',
            'text': 'This is a tweet.',
            'user': {
                'id_str': '67890',
                'screen_name': 'luke',
            },
        }
        self.assertEqual(msg['user'], self.messagetools.tweet_user(msg))

    def test_tweet_user_nontweet(self):
        """
        tweet_user() should rase `ValueError` for a non-tweet message.
        """
        msg = {'friends': []}
        self.assertRaises(ValueError, self.messagetools.tweet_user, msg)

    def test_is_user(self):
        """
        is_user() should return `True` for valid user data.
        """
        self.assertEqual(True, self.messagetools.is_user({
            'id_str': '12345',
            'screen_name': 'luke'
        }))

    def test_is_user_nontweet(self):
        """
        is_user() should return `False` for a non-tweet message.
        """
        self.assertEqual(False, self.messagetools.is_user({
            'friends': [],
        }))

    def test_ensure_user(self):
        """
        ensure_user() should return the original user data.
        """
        user = {
            'id_str': '12345',
            'screen_name': 'luke'
        }
        self.assertEqual(user, self.messagetools.ensure_user(user))

    def test_ensure_user_nonuser(self):
        """
        ensure_user() should rase `ValueError` for invalid user data.
        """
        self.assertRaises(ValueError, self.messagetools.ensure_user, {})

    def test_user_id(self):
        """
        user_id() should return the `id_str` field of a user.
        """
        user = {
            'id_str': '12345',
            'screen_name': 'luke'
        }
        self.assertEqual('12345', self.messagetools.user_id(user))

    def test_user_id_nonuser(self):
        """
        user_id() should rase `ValueError` for a non-tweet message.
        """
        self.assertRaises(ValueError, self.messagetools.user_id, {})

    def test_user_screen_name(self):
        """
        user_screen_name() should return the `screen_name` field of a user.
        """
        user = {
            'id_str': '12345',
            'screen_name': 'luke'
        }
        self.assertEqual('luke', self.messagetools.user_screen_name(user))

    def test_user_screen_name_nonuser(self):
        """
        user_screen_name() should rase `ValueError` for a non-tweet message.
        """
        self.assertRaises(ValueError, self.messagetools.user_screen_name, {})
