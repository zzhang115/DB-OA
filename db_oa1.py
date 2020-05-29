import re
RAW_NAMES = [
'SPV Inc., DBA: Super Company',
'Michael Forsky LLC d.b.a F/B Burgers .',
'*** Youthful You Aesthetics ***',
'Aruna Indika (dba. NGXess)',
'Diot SA, - D. B. A. *Diot-Technologies*',
'PERFECT PRIVACY, LLC, d-b-a Perfection,',
'PostgreSQL DB Analytics',
'/JAYE INC/',
' ETABLISSEMENTS SCHEPENS /D.B.A./ ETS_SCHEPENS',
'DUIKERSTRAINING OOSTENDE | D.B.A.: D.T.O. '
]
CLEANED_NAME_PAIRS = [
('SPV Inc', 'Super Company'),
('Michael Forsky LLC', 'F/B Burgers'),
('Youthful You Aesthetics', None),
('Aruna Indika', 'NGXess'),
('Diot SA', 'Diot-Technologies'),
('PERFECT PRIVACY, LLC', 'Perfection'),
('PostgreSQL DB Analytics', None),
('JAYE INC', None),
('ETABLISSEMENTS SCHEPENS', 'ETS SCHEPENS'),
('DUIKERSTRAINING OOSTENDE', 'D.T.O'),
]

def clean_names(raw_names):
    results = []
    if raw_names:
        for raw_name in raw_names:
            raw_name = re.sub(r'D[^A-Za-z]*B[^A-Za-z]*A[^A-Za-z]+', 'DBA:', raw_name, flags=re.IGNORECASE)
            names = raw_name.split('DBA:')
            legal_name = names[0]
            legal_name = re.sub(r'^[^A-Za-z]*(.+?)[^A-Za-z]*$', r'\1', legal_name)
            dba_name = None
            if len(names) > 1:
                dba_name = names[1]
                dba_name = re.sub(r'^[^A-Za-z]*(.+?)[^A-Za-z]*$', r'\1', dba_name)
                dba_name = re.sub(r'[_]+', ' ', dba_name)
            results.append((legal_name, dba_name))
    return results

assert clean_names(RAW_NAMES) == CLEANED_NAME_PAIRS
print('Matched with cleaned name pairs!')