from planmate.lib.helpers import AuthenticationHelper


def status(context, request):
  print 'AUTH STATUS', context, AuthenticationHelper.instance().get_user_id()
  is_logged_in = AuthenticationHelper.instance().is_logged_in()

  if not is_logged_in:
    return {'is_logged_in': is_logged_in}

  user = AuthenticationHelper.instance().get_user()
  user_dict = user.to_json()

  user_dict.update({
    'user_id': user.key.id(),
    'user_key': user.key.urlsafe(),
    'is_logged_in': is_logged_in
    })

  return user_dict


def logout(context, request):
  print 'LOGOUT', context

  AuthenticationHelper.instance().logout()
  return {}
