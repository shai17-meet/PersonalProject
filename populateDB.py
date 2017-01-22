from model import *
engine = create_engine('sqlite:///forum.db')
Base.metadata.create_all(engine)
Base.metadata.bind= engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()
newUser=User(name="Shai")
threads=[
{'title':'test 1', 'text':'this is a test'},
{'title':'test 2', 'text':'this is also a test'},
{'title':'test 3', 'text':'this is the final test'}
]
for thread in threads:
	newThread= Thread(title=thread['title'], text=thread['text'])
	session.add(newThread)
	session.commit()