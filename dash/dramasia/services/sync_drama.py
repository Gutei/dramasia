import base64
import requests
import uuid
from dramasia.models import Drama, DramaTag, Genre, DramaGenre, Cast, DramaCast
from django.core.files.base import ContentFile

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

            if drama_json['poster'] and drama_json['poster'] != '':
                drama_image_binary = base64.b64encode(requests.get(drama_json['poster']).content)
                data_poster = ContentFile(base64.b64decode(drama_image_binary), name='{}.{}'.format(mdl_id, drama_json['poster'].split('.')[-1]))


            drama = Drama(
                mdl_id=mdl_id,
                title=drama_json['title'],
                native_title=drama_json['native_title'],
                alias=",".join(drama_json['aka']),
                description=drama_json['synopsis'],
                image_url=drama_json['poster'],
                network=drama_json['network'],
                duration=drama_json['duration'],
                mdl_score=0 if not drama_json['score'] or drama_json['score'] == 'N/A' else drama_json['score'],
                rating='' if not drama_json['rating'] else drama_json['rating'],
                country='' if not drama_json['country'] else drama_json['country'],
                airing_date=drama_json['aired'],
                total_episode=drama_json['episodes'],
                image=data_poster,
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
                        img_name = uuid.uuid4()
                        cast_image_binary = base64.b64encode(requests.get(c['image']).content)
                        data_cast_img = ContentFile(base64.b64decode(cast_image_binary), name='{}.{}'.format(img_name.hex[:8], c['image'].split('.')[-1]))

                        cast = Cast(
                            image_url=c['image'],
                            name=cast_name,
                            image=data_cast_img,
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


