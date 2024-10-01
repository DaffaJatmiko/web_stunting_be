def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    
    # Child routes
    config.add_route('child', '/children')
    config.add_route('child_detail', '/children/{id}')
    
    # Health Record routes
    config.add_route('health_record', '/health-records/children/{children_id}')
    config.add_route('health_record_detail', '/health-records/{record_id}/children/{children_id}')
    
    # Measurement routes
    config.add_route('measurement', '/measurements/children/{children_id}')
    config.add_route('measurement_detail', '/measurements/{measurement_id}/children/{children_id}')