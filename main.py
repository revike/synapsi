from answers import oldest_actor, youngest_actor, old_oldest_actor, \
    old_youngest_actor, biggest_film, dead_longest_period, oldest_film, \
    actors_same_year, quantity_dead_actors, ave_age_live_actors, \
    ave_quantity_films
from constants import base_url, headers, password, login, first_name, \
    last_name, email, github
from session import SessionAPI


def main():
    """Run"""
    session = SessionAPI(base_url, login, password, headers)
    data = session.get_data()

    answers = {
        **oldest_actor(data),
        **youngest_actor(data),
        **old_oldest_actor(data),
        **old_youngest_actor(data),
        **biggest_film(data),
        **dead_longest_period(data),
        **oldest_film(data),
        **actors_same_year(data),
        **quantity_dead_actors(data),
        **ave_age_live_actors(data),
        **ave_quantity_films(data),
    }

    post_answer_data = {
        'first_name': first_name.title(),
        'last_name': last_name.title(),
        'email': email.lower(),
        'answers': answers
    }

    with open('file.txt', 'w', encoding='utf-8') as obj:
        obj.write(f'{post_answer_data}\n\n{github}\n')

    session.post_answer(post_answer_data)
    session.post_file()
    session.put_mark()


if __name__ == '__main__':
    main()
