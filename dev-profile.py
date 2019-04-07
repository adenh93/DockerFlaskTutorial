from webapp.blog.models import User, Post, Tag, db
from faker import Faker

faker = Faker()

USER_COUNT = 5
POST_COUNT = 10
TAG_COUNT = 3

def generate_tags():
    titles = ["Python", "Flask", "Webdev"]
    for i in range(TAG_COUNT):
        tag = Tag(title=titles[i])
        db.session.add(tag)
        db.session.commit()

def generate_dev_data():
    tags = Tag.query.all()
    for i in range(USER_COUNT):
        profile = faker.profile()
        user = User()
        user.username = profile["username"]
        user.email = profile["mail"]
        user.name = profile["name"]
        for i in range(POST_COUNT):
            post = Post()
            post.title = faker.text(max_nb_chars=40)
            post.body = faker.text(max_nb_chars=4000)
            for tag in tags:
                post.tags.append(tag)
            user.posts.append(post)
        db.session.add(user)
        db.session.commit()

generate_tags()
generate_dev_data()

