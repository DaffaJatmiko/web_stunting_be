def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    
    # Child routes
    config.add_route('child_list', '/children')
    config.add_route('child_detail', '/children/{id}')
    config.add_route('child_add', '/add/children')
    
    # Health Record routes
    config.add_route('health_record_list', '/children/{children_id}/health-records')
    config.add_route('health_record_detail', '/children/{children_id}/health-records/{record_id}')
    config.add_route('health_record_add', '/children/{children_id}/add/health-records')
    config.add_route('health_record_update', '/children/{children_id}/update/health-records/{record_id}')
    config.add_route('health_record_delete', '/children/{children_id}/delete/health-records/{record_id}')
    
    # Measurement routes
    config.add_route('measurement_list', '/children/{children_id}/measurements')
    config.add_route('measurement_detail', '/children/{children_id}/measurements/{measurement_id}')
    config.add_route('measurement_add', '/children/{children_id}/add/measurements')
    config.add_route('measurement_update', '/children/{children_id}/update/measurements/{measurement_id}')
    config.add_route('measurement_delete', '/children/{children_id}/delete/measurements/{measurement_id}')