from rest_framework import serializers

from .models import Voice, File, Song, Genre, Singer

"""
### Saving serializer (Create & Update)
# .save() will create a new instance.
serializer = CommentSerializer(data=tata)

# .save() will update the existing `comment` instance.
serializer = CommentSerializer(comment, data=data)

# Passing additional attributes to .save() which is not part of the request data
serializer.save(owner=request.user)


### Partial updates
# Update `comment` with partial data
serializer = CommentSerializer(comment, data={'content': 'foo bar'}, partial=True)
"""


class VoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Voice
        fields = ['user', 'max_pitch', 'min_pitch']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        request = self.context.get("request")
        voice = Voice.objects.create(**validated_data, user=request.user)

        return voice


# File upload 를 위한 serializer
class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ['id', 'filename', 'user']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        request = self.context.get("request")
        file = File.objects.create(**validated_data, user=request.user)

        return file


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'
        read_only_fields = ['id']


class SingerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Singer
        fields = '__all__'
        read_only_fields = ['id']


# writable nested representation
class SongSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(required=False, many=True)
    singer = SingerSerializer(required=False, many=True)

    class Meta:
        model = Song
        fields = ['title', 'max_pitch', 'min_pitch', 'singer', 'genre']
        read_only_fields = ['id']

    # 디폴트 ModelSerializer 의 .create(), .update() 메소드는 writable nested representations을 지원하지 않음
    # validated_data 에는 'title', 'max_pitch', 'min_pitch', 'singer', 'genre' 정보 담겨 있음
    def create(self, validated_data):
        genre_data = validated_data.pop('genre')    # genre 정보만 추출하여 genre_data에 담음
        singer_data = validated_data.pop('singer')  # singer 정보만 추출하여 singer_data에 담음

        all_genres = Genre.objects.all()
        all_singers = Singer.objects.all()

        genres = []
        singers = []

        for genre_object in genre_data:
            # 해당하는 genre 있으면 그 genre와 연결
            try:
                exist_genre = all_genres.get(name=genre_object['name'])
                genres.append(exist_genre)
            # 없으면 genre 생성
            except Genre.DoesNotExist:
                genres.append(Genre.objects.create(**genre_object))

        for singer_object in singer_data:
            # 해당하는 singer 있으면 그 singer와 연결
            try:
                exist_singer = all_singers.get(name=singer_object['name'], date_of_debut=singer_object['date_of_debut'])
                singers.append(exist_singer)
            # 없으면 singer 생성
            except Singer.DoesNotExist:
                singers.append(Singer.objects.create(**singer_object))

        # validated_data에는 title, max_pitch, min_pitch 가 남음
        song = Song.objects.create(**validated_data)        # Song 인스턴스 생성
        # Song 인스턴스에 genres, singers 연결
        song.genre.set(genres)
        song.singer.set(singers)
        return song

    def update(self, instance, validated_data):
        singer_data = validated_data.pop('singer')  # singer 정보만 추출하여 singer_data에 담음
        genre_data = validated_data.pop('genre')  # genre 정보만 추출하여 genre_data에 담음

        # Unless the application properly enforces that this field is
        # always set, the follow could raise a `DoesNotExist`, which
        # would need to be handled.
        singer = instance.singer
        genre = instance.genre

        instance.title = validated_data.get('title', instance.title)
        instance.max_pitch = validated_data.get('max_pitch', instance.max_pitch)
        instance.min_pitch = validated_data.get('min_pitch', instance.min_pitch)
        instance.save()

        singer.name = singer_data.get('name', singer.name)
        singer.date_of_debut = singer_data.get('date_of_debut', singer.date_of_debut)
        singer.save()

        genre.name = genre_data.get('name', genre.name)
        genre.save()

        return instance
