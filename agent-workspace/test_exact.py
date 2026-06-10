# Reproduce exactly the generator's f-string behavior
line_from_generator = '    std::string init_body = "{{\\"" + std::string(fcg) + "\\":\\"" + job->guid + "\\",\\"" + std::string(fcf) + "\\":\\"" + sbn + "\\",\\"" + std::string(fct) + "\\":" + std::to_string(total) + "}}";\n'
print('source repr:', repr(line_from_generator))
print('source bytes:', line_from_generator.encode('utf-8').hex())

# Now evaluate as f-string
result = eval(f"f'''{line_from_generator}'''")
print('result repr:', repr(result))
print('result bytes:', result.encode('utf-8').hex())

