ABOUT
=====

django_price is an attempt to implement price representation for django, done the
right way. Prices itself are very easy to implement, but may be done very
wrong if it comes to do calculations including tax (or multiple taxes).

django_price features a Price class to represent net/tax/gross prices. This
class may be added, multiplied, etc. like you would some "simple decimal"
expect to behave. Internaly however it keeps track of all applied taxes
and its corresponding net/tax/gross amounts. So adding two prices to
calculate the total of - for example - an invoice does not loose important
information (like which tax amounts are included).

WHY
===

As said above price calculation can go terribly wrong. This even happens for
big players like Magento (10€ product + 5€ shipping = 15.01€ for 19% tax, before Magento 1.8).
django_price tries to do things right to avoid such issues.

FEATURES
========

* Basic calculation for prices (including tax information)
* Knows the used currency (for rounding and formatting)
* Stores taxes to your database (LinearTax and Multitax)
* Proper rounding for prices (on demand, based on used currency)
* Utilities to:
  - Store prices to the database
  - Round prices based on the used currency

ROUNDING
========

django_price does implicit rounding when calculating the net/gross/tax amount
of prices. In addition the raw/precise values are stored internally. So when you calculate
with prices the calculations are always done using the precise prices, afterwards the rounded
results are recalculated.

If you need prices to stay stable (10 times 100 should be exactly 1000) you may
need to do explicit rounding. This should always happen when you need to display the
amounts to anyone.

REQUIREMENTS
============

* Django (obviously)
* django_deferred_polymorph (may be skipped if you don't use the supplied models)
