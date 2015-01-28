import json


def file_to_dict(filename):
    f = open(filename, 'r')
    correct_json = '[' + ','.join(f.readlines()) + ']'
    f.close()
    return json.loads(correct_json)

def filter_observations(areas, observations):
    area_codes = [area['iso3'] for area in areas]
    filtered_observations = [observation for observation in observations
                                        if 'code' in observation
                                        and observation['code'] in area_codes]
    return filtered_observations

def write_dict_to_file(dict, filename):
    f = open(filename, 'w')
    for item in dict:
        f.write(json.dumps(item) + '\n')
    f.close()


if __name__ == '__main__':
    areas = file_to_dict('areas.json')
    observations = file_to_dict('observations.json')
    filtered_observations = filter_observations(areas, observations)
    write_dict_to_file(filtered_observations, 'filtered_observations.json')
