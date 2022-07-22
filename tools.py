import numpy as np
from itertools import groupby

def length_last_streak(all_trials,current_trial,streak_type=1):
    """ Gives length of streak of streak_type preceding the current_trial
    Args:
        all_trials (numpy array): an array with all feddback for the session (+1/-1)
        current_trial (int): the index of the current trial
        streak_type (int, optional): type of streak to search for. Defaults to 1, aka reward, else -1 for failure

    Returns:
        len_last_streak:  length of streak of streak_type preceding the current_trial. None if not current type or streak length <2
    """
    len_last_streak = None
    grouped_before_index = [list(g) for k,g in groupby(all_trials[:current_trial])] #index is excluded
    if grouped_before_index[-1][0] == streak_type:
    
        if len(grouped_before_index[-1]) > 1:
            len_last_streak = len(grouped_before_index[-1])
    
    return len_last_streak