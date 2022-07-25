# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of primavera-dmt and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

"""
Standard vocabularies for the DMT
"""

CALENDARS = [
    ("standard", "standard"),
    ("gregorian", "gregorian"),
    ("proleptic_gregorian", "proleptic_gregorian"),
    ("noleap", "noleap"),
    ("365_day", "365_day"),
    ("360_day", "360_day"),
    ("julian", "julian"),
    ("all_leap", "all_leap"),
    ("366_day", "366_day"),
]


CHECKSUM_TYPES = [("SHA256", "SHA256"), ("MD5", "MD5"), ("ADLER32", "ADLER32")]
