import sqlite3


def get_all(query: str):

    with sqlite3.connect('netflix.db') as conn:
        conn.row_factory = sqlite3.Row
        result = []

        for item in conn.execute(query).fetchall():
            result.append(dict(item))

        return result


def get_one(query: str):

    with sqlite3.connect('netflix.db') as conn:
        conn.row_factory = sqlite3.Row
        result = conn.execute(query).fetchone()

        if result is None:
            return None
        else:
            return dict(result)


def search_pair(actor1, actor2):
    query = f"""
    SELECT * FROM netflix
    WHERE netflix."cast" LIKE '%{actor1}%' 
    AND netflix."cast" LIKE '%{actor2}%'
    """
    result = double_connect('netflix.db', query)
    result_list = []
    for line in result:
        line_list = line[0].split(',')
        result_list += line_list
    counter = Counter(result_list)
    actors_list = []
    for key, value in counter.items():
        if value > 2 and key.strip() not in [actor1, actor2]:
            actors_list.append(key)
    return actors_list


def get_movie_by_genre(type_movie, release_year, listed_in):
    query = f""" SELECT title, description FROM netflix
        WHERE "type" = '{type_movie}'
        AND release_year = '{release_year}'
        AND listed_in = '{listed_in}'
        """

    result = []

    for item in get_all(query):
        result.append(
            {
                'title': item['title'],
                'description': item['description']
            }
        )

    return result

