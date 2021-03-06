#!/usr/bin/env python3
'''
Testing of drift by a given controller, by reporting angular coordinates
'''

import time
from datetime import datetime
import config

# Calculate the drift in RA

def drift_test(iterations = 60, interval = 10):
  ra_min = 0.0
  count = 0

  print('Time            OnStep Time   Sidereal      St  RA            DE        Equ                  RAdlta RA"/min RA"Max DE"/min DE"Max')

  while True:
    # Increment the iteration counter
    count = count + 1
    # Check if we reached the maximum count, and exit
    if count > iterations:
      time.sleep(1)
      return

    curr_ra = config.scope.get_ra(True) # High precision coordinates
    curr_de = config.scope.get_de()
    equ_decimal  = config.scope.get_debug_equ()

    local_tm    = config.scope.get_time(True)
    dt          = datetime.now().strftime('%H:%M:%S.%f')
    sidereal_tm = config.scope.get_sidereal_time(True)

    status = 'N/A'
    if config.scope.is_slewing is True:
      status = 'SLW'

    if config.scope.is_tracking is True:
      status = 'TRK'

    ra = float(equ_decimal.split(',')[0])
    de = float(equ_decimal.split(',')[1])
    if ra_min == 0.0:
      # First pass, initialize values
      ra_min = ra
      ra_max = ra
      de_min = de
      de_max = de
      time_start = datetime.now()
      ra_arc_secs = 0.0
      de_arc_secs = 0.0
      ra_max_drift = 0.0
      de_max_drift = 0.0
      ra_drift = 0.0
      de_drift = 0.0
      ra_drift_per_min = 0.0
      de_drift_per_min = 0.0
      ra_prev = 0.0
      de_prev = 0.0
      ra_deviation = 0.0
      de_deviation = 0.0

    else:
      # Record maximums and minimums
      if ra_prev == 0.0:
        ra_prev = ra
      if de_prev == 0.0:
        de_prev = de

      ra_deviation = (ra - ra_prev) / 0.000278
      de_deviation = (de - de_prev) / 0.000278

      ra_prev = ra
      de_prev = de

      if ra < ra_min:
        ra_min = ra
      if ra > ra_max:
        ra_max = ra

      if de < de_min:
        de_min = de
      if de > de_max:
        de_max = de

      # Calculate elapsed time
      time_now = datetime.now()
      elapsed = (time_now - time_start)
      secs = elapsed.seconds

      # calculate drift
      ra_drift = (ra_max - ra_min) / 0.000278
      de_drift = (de_max - de_min) / 0.000278

      ra_arc_secs = ra_drift / (secs / 60)
      de_arc_secs = de_drift / (secs / 60)

    # format results
    ra_drift_per_min = '{:6.2f}'.format(ra_arc_secs)
    de_drift_per_min = '{:6.2f}'.format(de_arc_secs)

    ra_max_drift = '{:6.2f}'.format(ra_drift)
    de_max_drift = '{:6.2f}'.format(de_drift)

    ra_dev = '{:6.2f}'.format(ra_deviation)
    de_dev = '{:6.2f}'.format(de_deviation)

    print('%s %s %s %s %s %s %s %s %s %s %s %s' % (dt, local_tm, sidereal_tm, status, curr_ra, curr_de, equ_decimal, ra_dev, ra_drift_per_min, ra_max_drift, de_drift_per_min, de_max_drift))
    
    try:
      time.sleep(interval)
    except KeyboardInterrupt:
      print('Exiting ...')
      time.sleep(1)
      return
