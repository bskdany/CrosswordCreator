import configparser
config = configparser.ConfigParser()
config['DEFAULT'] = {
    'words': {'this',
            'thing',
            'somehow',
            'makes',
            'crosswords'
            },
    'how_many_crosswords': '1',
    'size' : '20'


} 

with open('config.ini', 'w') as configfile:
    config.write(configfile)