test = {   'name': 'q8b',
    'points': 1,
    'suites': [   {   'cases': [   {   'code': '>>> training_error > 0\nTrue',
                                       'hidden': False,
                                       'locked': False},
                                   {   'code': '>>> test_error > 0\nTrue',
                                       'hidden': False,
                                       'locked': False},
                                   {   'code': '>>> np.isclose(training_error, '
                                               '46710.5975, atol=0.1) or '
                                               'np.isclose(training_error, '
                                               '32163.67775, atol=0.1) # 1st '
                                               'case correct, 2nd case if '
                                               'switched root & mean in rmse '
                                               "(our public tests didn't "
                                               'verify)\n'
                                               'True',
                                       'hidden': True,
                                       'locked': False},
                                   {   'code': '>>> np.isclose(test_error, '
                                               '46146.6426, atol=0.1) or '
                                               'np.isclose(test_error, '
                                               '32788.74734, atol=0.1) # 1st '
                                               'case correct, 2nd case if '
                                               'switched root & mean in rmse '
                                               "(our public tests didn't "
                                               'verify)\n'
                                               'True',
                                       'hidden': True,
                                       'locked': False}],
                      'scored': True,
                      'setup': '',
                      'teardown': '',
                      'type': 'doctest'}]}
