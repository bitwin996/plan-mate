from google.appengine.ext import ndb


class Base(object):
  # accept: parent
  def __init__(self, *args, **options):
    self.request = args[0]
    self.__parent__ = options.pop('parent', None)
    self.__name__   = options.pop('name', None)

  def get_parent_key(self):
    if hasattr(self.__parent__, 'key'):
      return self.__parent__.key

  def get_model(self):
    if hasattr(self, 'model'):
      return self.model
    elif hasattr(self.__class__, 'model'):
      return self.__class__.model

  def get_key(self):
    if hasattr(self, 'key'):
      return self.key

  def create_key(self, model, unicode_id, parent_key=None):
    # id
    if not unicode.isnumeric(unicode_id):
      return KeyError
    int_id = int(unicode_id)

    # parent key
    key_options = {}
    parent_key = self.get_parent_key()
    if parent_key: key_options['parent'] = parent_key

    key = ndb.Key(model, int_id, parent=parent_key)
    return key


class Model(Base):
  pass


class Entity(Base):
  def __init__(self, *args, **options):
    if not options.has_key('key'):
      raise NotImplementedError()
    self.key = options.pop('key')
    self.__name__ = self.key.id()

    super(Entity, self).__init__(*args, **options)

