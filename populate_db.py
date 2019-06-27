import datetime
from ennead.config import Config

from ennead.models.base import database
from ennead.models.user import User, UserGroup
from ennead.models.task import TaskSet, Task
from ennead.models.thread import Thread, Post
from ennead.models.file import File

config_path = 'ennead.json'
if config_path:
    config = Config.from_filename(config_path)
else:
    config = Config()

database.initialize(config.DB_CLASS(config.DB_NAME, **config.DB_PARAMS))
database.create_tables([User, Task, TaskSet, Thread, Post, File])

student = User(
    username = 'test',
    email = 'test@test.com',
    registered_at = datetime.datetime.now(),
    first_name = 'Иван',
    surname = 'Петров',
    patronym = 'Иванович',
    group = UserGroup.student)
student.set_password('password')
student.save()

teacher = User(
    username = 'prep',
    email = 'prep@test.com',
    registered_at = datetime.datetime.now(),
    first_name = 'Препод',
    surname = 'Злой',
    patronym = '',
    group = UserGroup.teacher)
teacher.set_password('password')
teacher.save()


prev_task_set = TaskSet.create(name='Старая заочка', active=True)
task_set = TaskSet.create(name='Текущая заочка', active=True)

task_1_1 = Task.create(order_num=1, name='Очень старая задача #1', description='Когда трава была зеленее', solution="Как-нибудь проверим", base_score=1, task_set=prev_task_set)
task_1_2 = Task.create(order_num=2, name='Очень старая задача #2', description='И задачи были забористей', solution="Как-нибудь проверим", base_score=1, task_set=prev_task_set)

task_2_1 = Task.create(order_num=1, name='Задача первая', description='Начнём с простого: $$2+2=?$$', solution="Ноль баллов обычно.\nПолный балл за $$2+2=4$$", base_score=1, task_set=task_set)
task_2_2 = Task.create(order_num=3, name='Задача последняя', description='Хардкор', solution="Как-нибудь проверим", base_score=42, task_set=task_set)
task_2_3 = Task.create(order_num=2, name='Задача два', description='Посложнее', solution="Как-нибудь проверим", base_score=5, task_set=task_set)

thread_1 = Thread.create(student=student, task=task_2_1)
thread_2 = Thread.create(student=student, task=task_2_2)

post_1_1 = Post.create(thread=thread_1, text='Первый коммент', date = datetime.datetime.now(), author=student)
post_1_2 = Post.create(thread=thread_1, text='Так себе "решение". Пока 0 баллов', date = datetime.datetime.now(), author=teacher)
post_1_3 = Post.create(thread=thread_1, text='Ну ладно, \\(2+2=3\\)', date = datetime.datetime.now(), author=student)
post_1_3 = Post.create(thread=thread_1, text='Ой, $$2+2=4$$', date = datetime.datetime.now(), author=student)
post_1_4 = Post.create(thread=thread_1, text='Это вот серьёзно сейчас было?', hide_from_student=True, date = datetime.datetime.now(), author=teacher)
post_1_5 = Post.create(thread=thread_1, text='Ок, угадал. 1 балл', date = datetime.datetime.now(), author=teacher)
