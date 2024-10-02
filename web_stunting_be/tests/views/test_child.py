import unittest
from unittest.mock import Mock, patch
from pyramid import testing
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from sqlalchemy.exc import IntegrityError

from web_stunting_be.views.child import ChildViews, ChildDetailViews

class TestChildViews(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.request = testing.DummyRequest()
        self.request.dbsession = Mock()

    def tearDown(self):
        testing.tearDown()

    @patch('web_stunting_be.models.child.Child.get_all')
    def test_list(self, mock_get_all):
        mock_get_all.return_value = [Mock(to_dict=lambda: {'id': 1})]
        view = ChildViews(self.request)
        response = view.list()
        self.assertEqual(len(response['data']), 1)
        self.assertEqual(response['total'], 1)

    @patch('web_stunting_be.models.child.Child.create')
    def test_add(self, mock_create):
        mock_create.return_value = Mock(children_id=1)
        self.request.json_body = {'name': 'Test Child'}
        view = ChildViews(self.request)
        response = view.add()
        self.assertEqual(response['children_id'], 1)

    @patch('web_stunting_be.models.child.Child.create')
    def test_add_key_error(self, mock_create):
        mock_create.side_effect = KeyError('name')
        self.request.json_body = {}
        view = ChildViews(self.request)
        response = view.add()
        self.assertIsInstance(response, HTTPBadRequest)

    @patch('web_stunting_be.models.child.Child.create')
    def test_add_integrity_error(self, mock_create):
        mock_create.side_effect = IntegrityError(None, None, None)
        self.request.json_body = {'name': 'Test Child'}
        view = ChildViews(self.request)
        response = view.add()
        self.assertIsInstance(response, HTTPBadRequest)

class TestChildDetailViews(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.request = testing.DummyRequest()
        self.request.dbsession = Mock()
        self.request.matchdict = {'id': '1'}

    def tearDown(self):
        testing.tearDown()

    @patch('web_stunting_be.models.child.Child.get_by_id')
    def test_detail(self, mock_get_by_id):
        mock_get_by_id.return_value = Mock(to_dict=lambda: {'id': 1})
        view = ChildDetailViews(self.request)
        response = view.detail()
        self.assertEqual(response['id'], 1)

    @patch('web_stunting_be.models.child.Child.get_by_id')
    def test_detail_not_found(self, mock_get_by_id):
        mock_get_by_id.return_value = None
        view = ChildDetailViews(self.request)
        response = view.detail()
        self.assertIsInstance(response, HTTPNotFound)

    @patch('web_stunting_be.models.child.Child.update')
    def test_update(self, mock_update):
        mock_update.return_value = Mock(children_id=1)
        self.request.json_body = {'name': 'Updated Child'}
        view = ChildDetailViews(self.request)
        response = view.update()
        self.assertEqual(response['children_id'], 1)

    @patch('web_stunting_be.models.child.Child.delete')
    def test_delete(self, mock_delete):
        mock_delete.return_value = True
        view = ChildDetailViews(self.request)
        response = view.delete()
        self.assertEqual(response['children_id'], 1)

    @patch('web_stunting_be.models.child.Child.delete')
    def test_delete_not_found(self, mock_delete):
        mock_delete.return_value = False
        view = ChildDetailViews(self.request)
        response = view.delete()
        self.assertIsInstance(response, HTTPNotFound)

if __name__ == '__main__':
    unittest.main()