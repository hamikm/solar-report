# Enphase Reports
Gets solar energy production, household consumption, and net household consumption from Enphase Enlighten.

## Usage
```
$ virtualenv env
$ . env/bin/activate
$ pip install -r requirements.txt
$ python report.py --start 3/4/20 --end 4/2/20

off peak consumption (< 08:00)          383.2 kwh
super off consumption (< 16:00)         221.1 kwh
peak consumption (< 21:00)              218.8 kwh

off peak production (< 08:00)           9.3 kwh
super off production (< 16:00)          781.5 kwh
peak production (< 21:00)               97.2 kwh

off peak net (< 08:00)                  373.9 kwh
super off net (< 16:00)                 -560.3 kwh
peak net (< 21:00)                      121.5 kwh
```

Follow the [Enphase API Quickstart](https://developer.enphase.com/docs/quickstart.html) and replace `ENPHASE_APP_KEY`, `ENPHASE_USER_ID`, and `ENPHASE_SYSTEM_ID` in the script to hook up your own system.

This script uses the SoCal Edison time of use 4-9 rate plan (TOU-D-4-9). Change `OFF_PEAK_END_HR`, `SUPER_OFF_PEAK_END_HR`, `PEAK_END_HR` for different rate plans.

## Pictures from my first "physical" side project
I installed my own 6.8 kW solar panel system in 2019 to take advantage of the 30% federal tax credit before it dropped. Not including four weekends of labor, it cost $11,200 after the credit and will pay itself off in about five years.

I modeled my permit application after a friend's, which made the whole permitting ordeal considerably more tractable than it would otherwise have been. Even so, it took about sixteen hours to design my system and write my permit, which was — somehow? — stamped on my first try. Inspection was also unexpectedly straightforward: after glacing at my electrical panel, the inspector signed off without even going on my roof! He said, "all those guys do a good job anyway." I held my tongue.

It took another several hours to finish my permission-to-operate application with SoCal Edison (SCE) and opt into net metering and time-of-use billing, which is required for net metering clients. I got an unexpectedly high first bill; my energy is _delivered_ by SCE but _generated_ by Clean Power Alliance (CPA). CPA has a surplus of solar energy, so it charges a negative super off peak rate. After switching over to SCE for generation, my already-improved electrical bill improved by nearly $50 per month.

![alt text](/imgs/solar1.jpg)
I built a trellis/ramp to make it easier to get twenty-one 50 lb panels on my roof.

![alt text](/imgs/solar2.jpg)
It took an entire day for me to find rafters and plan my roof penetrations with sidewalk chalk.

![alt text](/imgs/solar3.jpg)
Those boards on the rails on Enphase Microinverters.

![alt text](/imgs/solar4.jpg)
Here's the roof part of the finished product!

![alt text](/imgs/solar5.jpg)
Here's the ground part! The Enphase Envoy is on the left. It combines the two home runs from the roof, uses current transformers to monitor production and consumption, and reports those numbers at 15 minute intervals to the cloud.
