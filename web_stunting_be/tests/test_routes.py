import unittest
from pyramid import testing
from web_stunting_be import routes

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        routes.includeme(self.config)

    def tearDown(self):
        testing.tearDown()

    def test_routes_included(self):
        expected_routes = [
            'home',
            'child',
            'child_detail',
            'health_record',
            'health_record_detail',
            'measurement',
            'measurement_detail'
        ]

        mapper = self.config.get_routes_mapper()
        for route_name in expected_routes:
            route = mapper.get_route(route_name)
            self.assertIsNotNone(route, f"Route {route_name} not found")

    def test_route_patterns(self):
        route_patterns = {
            'home': '/',
            'child': '/children',
            'child_detail': '/children/{id}',
            'health_record': '/health-records/children/{children_id}',
            'health_record_detail': '/health-records/{record_id}/children/{children_id}',
            'measurement': '/measurements/children/{children_id}',
            'measurement_detail': '/measurements/{measurement_id}/children/{children_id}'
        }

        mapper = self.config.get_routes_mapper()
        for route_name, expected_pattern in route_patterns.items():
            route = mapper.get_route(route_name)
            self.assertIsNotNone(route, f"Route {route_name} not found")
            self.assertEqual(route.pattern, expected_pattern, 
                             f"Incorrect pattern for route {route_name}")

if __name__ == '__main__':
    unittest.main()