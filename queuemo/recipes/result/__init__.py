# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Result view
===========

The result view contains a page based analysis of the document. The view
is generated after running all the linters. This view is presented as
main view to the user.

Requirements:

* The result view must be able to continously procudes new linting.
  Therfore the view must be updateable and the new findings should come
  in as messages which increases the error counter.

* There are no hard timing requirements, but 5 minutes must be the upper
  limit to have a nice user experience.

Features:

* Table of content

"""
