# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# from queuemo.recipes import copy
# from queuemo.recipes import decider_fonts
# from queuemo.recipes import feedback_decider_fonts
# from queuemo.recipes import publish

# DECIDER_FONTS_IN = 'decider_fonts_input'

# def require():
#     return 'rawmaker'

# def before(rawspace: str):
#     copy(rawspace, '../config', DECIDER_FONTS_IN)
#     copy(rawspace, 'rawmaker', DECIDER_FONTS_IN)

# def run(rawspace: str):
#     decider_fonts(rawspace, DECIDER_FONTS_IN, DECIDER_FONTS_IN)

#     feedback_decider_fonts(rawspace, DECIDER_FONTS_IN, DECIDER_FONTS_IN)

# def after(rawspace: str):
#     # TODO: replace with public vars of feedback_decider_border!
#     fonts_used = DECIDER_FONTS_IN + '/feedback_decider_fonts__iamugly_view_used.html'
#     publish(rawspace, fonts_used, 'layout/fonts/used')

#     ugly_fonts = DECIDER_FONTS_IN + '/feedback_decider_fonts__iamugly_view_ugly.html'
#     publish(rawspace, ugly_fonts, 'layout/fonts/ugly')
