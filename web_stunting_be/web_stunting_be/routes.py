def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    
    # Child routes
    config.add_route('child', '/children')
    config.add_route('child_detail', '/children/{id}')
    
    # Health Record routes
    config.add_route('health_record', '/children/{children_id}/health-records')
    config.add_route('health_record_detail', '/children/{children_id}/health-records/{record_id}')
    
    # Measurement routes
    config.add_route('measurement', '/children/{children_id}/measurements')
    config.add_route('measurement_detail', '/children/{children_id}/measurements/{measurement_id}')