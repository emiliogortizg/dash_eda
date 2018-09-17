# -*- coding: utf-8 -*-

from pandas.api.types import is_numeric_dtype


def get_feature_type(dataframe, column_name):
    '''
        Function to obtain the type of a column in a dataframe
        distinguishing between 'categorical' and 'quantitative' variables
    '''
    type_ = 'categorical'
    if is_numeric_dtype(dataframe[column_name]):
        type_ = 'quantitative'
    return type_


def get_feature_and_axis(dataframe, column_name, axis_mode):
    '''
        Transform a column from a dataframe to the
        format (values and axis) required in a Scatter plot
    '''
    type_ = get_feature_type(dataframe, column_name)
    axis = {'title': column_name}
    if type_ == 'quantitative':
        values = dataframe[column_name]
        axis.update({
            'type': 'linear' if axis_mode == 'Linear' else 'log'
        })
    else:
        values = dataframe[column_name].copy()
        values[values.isnull()] = 'NaN'
        axis.update({
            'type': 'category',
            'categoryorder': 'array',
            'categoryarray': values.value_counts().keys()
        })
    return values, axis
