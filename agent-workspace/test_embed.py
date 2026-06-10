result = f'''std::string init_body = "{{\"" + std::string(fcg) + "\":\"" '''
print('embed result:', repr(result))
print('embed bytes:', result.encode('utf-8').hex())
