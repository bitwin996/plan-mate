from google.appengine.ext import ndb

from planmate.lib.helpers import AuthenticationHelper
from planmate.lib.exceptions import AppNotLoginError


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

  #def create_key(self, model, unicode_id, parent_key=None):
  def create_key(self, *args, **options):
    (model, unicode_id,) = args

    # id
    if not unicode.isnumeric(unicode_id): raise KeyError
    int_id = int(unicode_id)

    # parent key
    key_options = {}
    parent_key = self.get_parent_key()
    if parent_key: key_options['parent'] = parent_key

    key = ndb.Key(model, int_id, parent=parent_key)
    return key


class ModelResource(BaseResource):
  def _get_new_entity(self, *args, **options):
    model = self.get_model()

    features = options.pop('features', [])
    #list_args = list(args)

    add_parent = options.pop('add_parent', True)
    if add_parent and not options.has_key('parent'):
      parent_key = self.get_parent_key()
      options['parent'] = parent_key

    if options.has_key('current_user_key'):
      current_user_key = AuthenticationHelper.instance().get_user_key()
      if not current_user_key:
        raise AppNotLoginError()
      prop_name = options.pop('current_user_key')
      options[prop_name] = current_user_key
      #setattr(new_entity, prop_name, current_user_key)

    new_entity = model(*args, **options)
    return new_entity


  # This method should be implemented in subclasses
  def get_new_entity(self):
    raise NotImplementedError()

  def generate_key(self, unicode_id, **options):
    if not unicode.isnumeric(unicode_id):
      raise KeyError
    int_id = int(unicode_id)

    key = ndb.Key(self.get_model(), int_id, **options)
    return key

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

  def get_key(self):
    if hasattr(self, 'key'):
      return self.key


class OptionsResource(object):
  def __init__(self, request, name='', parent=None):
    self.request = request
    self.__name__ = name
    self.__parent__ = parent

  def __getitem__(self, name):
    return self.__class__(self.request, name, self)

