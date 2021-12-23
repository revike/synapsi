from datetime import datetime, date

date_today = datetime.now().date()


def convert_str_to_date(date_str: str):
    """Convert string to date"""
    return datetime.strptime(date_str, '%d-%m-%Y').date()


def calculate_age(birth, date_dod=None):
    """Calculate age"""
    if date_dod:
        return date_dod.year - birth.year - (
                (date_dod.month, date_dod.day) < (birth.month, birth.day))
    return date_today.year - birth.year - (
            (date_today.month, date_today.day) < (birth.month, birth.day))


def oldest_actor(data_json):
    """1. Who is the oldest actor (all actors)?"""
    result = {'1': []}
    result_date = {}
    birth_oldest_actor = date_today
    for data in data_json:
        date_birth = convert_str_to_date(data['dob'])
        if date_birth < birth_oldest_actor:
            birth_oldest_actor = date_birth
            result_date['1'] = data['name']
            result_date['dob'] = data['dob']
    for data in data_json:
        if data['dob'] == result_date['dob']:
            result['1'].append(data['name'])
    if len(result['1']) == 1:
        result['1'] = ''.join(result['1'])
    return result


def youngest_actor(data_json):
    """2. Who is the youngest actor?"""
    result = {'2': []}
    result_date = {}
    birth_youngest_actor = convert_str_to_date(data_json[0]['dob'])
    for data in data_json:
        date_birth = convert_str_to_date(data['dob'])
        if date_birth > birth_youngest_actor:
            birth_youngest_actor = date_birth
            result_date['2'] = data['name']
            result_date['dob'] = data['dob']
    for data in data_json:
        try:
            if data['dob'] == result_date['dob']:
                result['2'].append(data['name'])
        except KeyError:
            result['2'].append(data_json[0]['name'])
            break
    if len(result['2']) == 1:
        result['2'] = ''.join(result['2'])
    return result


def old_oldest_actor(data_json):
    """3. How old is the oldest actor?"""
    result = {}
    for data in data_json:
        if data['name'] == oldest_actor(data_json)['1']:
            date_dob = convert_str_to_date(data['dob'])
            try:
                date_dod = convert_str_to_date(data['dod'])
                calc_age = calculate_age(date_dob, date_dod)
            except (KeyError, ValueError):
                calc_age = calculate_age(date_dob)
            result['3'] = f'{calc_age}'
            break
    return result


def old_youngest_actor(data_json):
    """4. How old is the youngest actor?"""
    result = {}
    for data in data_json:
        if data['name'] == youngest_actor(data_json)['2']:
            date_dob = convert_str_to_date(data['dob'])
            try:
                date_dod = convert_str_to_date(data['dod'])
                calc_age = calculate_age(date_dob, date_dod)
            except (KeyError, ValueError):
                calc_age = calculate_age(date_dob)
            result['4'] = f'{calc_age}'
            break
    return result


def biggest_film(data_json):
    """5. Who has the biggest filmography?"""
    result = {'5': []}
    quantity_films = 0
    for data in data_json:
        if len(data['movies']) >= quantity_films:
            quantity_films = len(data['movies'])
    for data in data_json:
        if len(data['movies']) == quantity_films:
            result['5'].append(data['name'])
    if len(result['5']) == 1:
        result['5'] = ''.join(result['5'])
    return result


def dead_longest_period(data_json):
    """6. Who's dead for the longest period of time?"""
    result = {'6': []}
    period = 0
    for data in data_json:
        data_dob = convert_str_to_date(data['dob'])
        try:
            data_dod = convert_str_to_date(data['dod'])
            days = (data_dod - data_dob).days
            if days > period:
                period = days
        except (KeyError, ValueError):
            pass
    for data in data_json:
        data_dob = convert_str_to_date(data['dob'])
        try:
            data_dod = convert_str_to_date(data['dod'])
            days = (data_dod - data_dob).days
            if days == period:
                result['6'].append(data['name'])
        except (KeyError, ValueError):
            pass
    if len(result['6']) == 1:
        result['6'] = ''.join(result['6'])
    return result


def oldest_film(data_json):
    """7. Which movie is the oldest one?"""
    result = {'7': []}
    result_date = {}
    oldest_film_year = date_today.year + 1
    for data in data_json:
        for date_movies in data['movies']:
            try:
                year = int(str(date_movies['year']).strip())
                if oldest_film_year > date(year=year, month=1, day=1).year:
                    oldest_film_year = year
                    result_date[date_movies['title']] = oldest_film_year
            except (KeyError, TypeError, ValueError):
                pass
    for film, year in result_date.items():
        if year == oldest_film_year:
            result['7'].append(film)
    if len(result['7']) == 1:
        result['7'] = ''.join(result['7'])
    return result


def actors_same_year(data_json):
    """8. List the actors born in the same year (if any)."""
    result = {}
    result_value = {}
    years_list = []
    for data in data_json:
        years_list.append(data['dob'].split('-')[-1])
    years = [x for x in years_list if years_list.count(x) >= 2]
    for data in data_json:
        if data['dob'].split('-')[-1] in years:
            try:
                result_value[data['dob'].split('-')[-1]].append(
                    data['name'].replace('\n', ' ').replace('\t', ' '))
            except KeyError:
                result_value[data['dob'].split('-')[-1]] = []
                result_value[data['dob'].split('-')[-1]].append(
                    data['name'].replace('\n', ' ').replace('\t', ' '))
    result['8'] = result_value
    if not result['8']:
        result['8'] = None
    return result


def quantity_dead_actors(data_json):
    """9. How many dead actors do we have in the dataset?"""
    quantity = 0
    for data in data_json:
        try:
            convert_str_to_date(data['dod'])  # date_check
            quantity += 1
        except (KeyError, ValueError):
            pass
    return {'9': f'{quantity}'}


def ave_age_live_actors(data_json):
    """10. What's the average age of alive actors in the dataset?"""
    age = 0
    i = 0
    for data in data_json:
        try:
            convert_str_to_date(data['dod'])  # date_check
        except (KeyError, ValueError):
            date_birth = convert_str_to_date(data['dob'])
            age += calculate_age(date_birth)
            i += 1
    result = {'10': f'{"%.0f" % (age / i)}'}
    return result


def ave_quantity_films(data_json):
    """11. What's the average number of movies per actor?"""
    quantity_films = 0
    quantity_actors = 0
    for data in data_json:
        quantity_actors += 1
        quantity_films += len(data['movies'])
    result = {'11': f'{round(quantity_films / quantity_actors, 2)}'}
    return result
