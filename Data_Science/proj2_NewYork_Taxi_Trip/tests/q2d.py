test = {   'name': 'q2d',
    'points': 2,
    'suites': [   {   'cases': [   {   'code': '>>> np.isclose(s[0], '
                                               '0.02514825, 1e-3)\n'
                                               'True',
                                       'hidden': False,
                                       'locked': False},
                                   {   'code': '>>> train.shape\n(53680, 16)',
                                       'hidden': False,
                                       'locked': False},
                                   {   'code': '>>> test.shape\n(13421, 16)',
                                       'hidden': False,
                                       'locked': False},
                                   {   'code': ">>> list(train['region'][:8])\n"
                                               '[1, 1, 0, 1, 2, 1, 1, 0]',
                                       'hidden': False,
                                       'locked': False},
                                   {   'code': ">>> list(test['region'][:8])\n"
                                               '[2, 1, 2, 0, 1, 0, 1, 2]',
                                       'hidden': False,
                                       'locked': False},
                                   {   'code': '>>> '
                                               "sum(train[train['region']==1]['duration'])\n"
                                               '11666210',
                                       'hidden': False,
                                       'locked': False},
                                   {   'code': '>>> '
                                               "sum(test[test['region']==1]['duration'])\n"
                                               '2897696',
                                       'hidden': False,
                                       'locked': False}],
                      'scored': True,
                      'setup': '',
                      'teardown': '',
                      'type': 'doctest'}]}
