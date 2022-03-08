test = {   'name': 'q2',
    'points': 2,
    'suites': [   {   'cases': [   {   'code': '>>> isinstance(q2house1, (int, '
                                               'np.integer)) # Make sure your '
                                               'answer is integer-valued\n'
                                               'True',
                                       'hidden': False,
                                       'locked': False},
                                   {   'code': '>>> isinstance(q2house2, (int, '
                                               'np.integer)) # Make sure your '
                                               'answer is integer-valued\n'
                                               'True',
                                       'hidden': False,
                                       'locked': False},
                                   {   'code': ">>> min(training_data['PID']) "
                                               '<= min(q2house1, q2house2)\n'
                                               'True',
                                       'hidden': False,
                                       'locked': False},
                                   {   'code': ">>> max(training_data['PID']) "
                                               '>= max(q2house1, q2house2)\n'
                                               'True',
                                       'hidden': False,
                                       'locked': False},
                                   {   'code': '>>> '
                                               "sorted(set(training_data.loc[training_data['Gr_Liv_Area'] "
                                               "> 5000, 'PID']))\n"
                                               '[908154195, 908154235]',
                                       'hidden': True,
                                       'locked': False}],
                      'scored': True,
                      'setup': '',
                      'teardown': '',
                      'type': 'doctest'}]}
