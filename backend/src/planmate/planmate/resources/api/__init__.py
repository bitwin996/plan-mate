from google.appengine.ext import ndb

from planmate.lib.helpers import AuthenticationHelper


class BaseResource(object):
  _render_options = {}

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
      raise KeyError
    int_id = int(unicode_id)

    # parent key
    key_options = {}
    parent_key = self.get_parent_key()
    if parent_key: key_options['parent'] = parent_key

    key = ndb.Key(model, int_id, parent=parent_key)
    return key


class ModelResource(BaseResource):
  def _get_new_entity(self):
    model = self.get_model()
    parent_key = self.get_parent_key()

    new_entity = model(parent=parent_key)
    return new_entity

  def _get_new_entity_with_current_user_key(self, property_name='user_key'):
    new_entity = self._get_new_entity()

    current_user_key = AuthenticationHelper.instance().get_user_key()
    if not current_user_key:
      raise HTTPUnauthorized('Need to log in.')
    setattr(new_entity, property_name, current_user_key)

    return new_entity

  def get_new_entity(self):
    raise NotImplementedError()


  def get_query(self, *args, **options):
    return self._get_query(*args, **options)

  def _get_query(self, *args, **options):
    model = self.get_model()
    options['ancestor'] = self.get_parent_key()
    query = model.query(*args, **options)
    return query


class EntityResource(BaseResource):
  def __init__(self, *args, **options):
    if not options.has_key('key'):
      raise NotImplementedError()
    self.key = options.pop('key')
    self.__name__ = self.key.id()

    super(EntityResource, self).__init__(*args, **options)


class OptionsResource(object):
  def __init__(self, request, name='', parent=None):
    self.request = request
    self.__name__ = name
    self.__parent__ = parent

  def __getitem__(self, name):
    return self.__class__(self.request, name=name, parent=self)

