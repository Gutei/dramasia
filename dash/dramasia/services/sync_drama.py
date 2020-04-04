import requests
from dramasia.models import Drama, DramaTag, Genre, DramaGenre, Cast, DramaCast

def get_data_mdl(mdl_id):

    token = "vpTQzYIYKe584wd8yYrxeNY7kUpz7zKC"
    url = "https://service.inzpi.com/media-api/mydramalist/v1/{}/".format(mdl_id)

    data = requests.get(url, params={'token':token})

    if data.status_code == 200:
        drama_json = data.json()

        if drama_json['title']:
            drama = Drama.objects.filter(mdl_id=mdl_id).first()
            if drama:
                return None

            drama = Drama(
                mdl_id=mdl_id,
                title=drama_json['title'],
                native_title=drama_json['native_title'],
                alias=",".join(drama_json['aka']),
                description=drama_json['synopsis'],
                image_url=drama_json['poster'],
                network=drama_json['network'],
                duration=drama_json['duration'],
                mdl_score=0 if not drama_json['score'] else drama_json['score'],
                rating='' if not drama_json['rating'] else drama_json['rating'],
                country='' if not drama_json['country'] else drama_json['country'],
                airing_date=drama_json['aired'],
                total_episode=drama_json['episodes']
            )

            drama.save()

            for g in drama_json['genres'].split(', '):
                genre = Genre.objects.filter(genre=g).first()
                if not genre:
                    genre = Genre(genre=g)
                    genre.save()

                drama_genre = DramaGenre(drama=drama, genre=genre)
                drama_genre.save()

            for t in drama_json['tags']:
                drama_tag = DramaTag(
                    drama=drama,
                    tag=t.replace('  (Vote or add tags)','')
                )

            for c in drama_json['cast']:
                if c['image']:
                    cast = Cast.objects.filter(image_url=c['image']).first()
                    act_name = c['name'].split(' in ')
                    if not cast:
                        cast_name = act_name[0]
                        cast = Cast(
                            image_url=c['image'],
                            name=cast_name
                        )
                        cast.save()

                    drama_cast = DramaCast(
                        drama=drama,
                        cast=cast,
                        role=c['role'],
                        cast_as=c['as']
                    )
                    drama_cast.save()

    return None


