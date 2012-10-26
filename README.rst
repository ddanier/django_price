ABOUT
=====

django_price is an attempt to implement price representation in django, the
right way. Prices itself are very easy to implement, but may be done very
wrong if it comes to do calculations including tax.

django_price features a Price class to represent net/tax/gross prices. This
class may be added, multiplied, ... like you would some "simple decimal"
expect to behave. Internaly however it keeps track of all applied taxes
and its corresponsing net/tax/groos amounts. So adding two prices to
calculate the total of - for example - an invoice does not loose important
information (like which tax amounts are included).

WHY
===

As said above price calculation can go terribly wrong. This even happens for
big players like Magento (10€ product + 5€ shipping = 15.01€ for 19% tax).
django_price tries to do things right, to avoid such issues.

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

django_price does implicid rounding when calculating the net/gross/tax amount
of prices. In addition the raw, precise values are stored. So when you calculate
with prices this is always done using the precise prices, afterwards the rounded
results are recalculated.

If yoou need prices to stay stable (10 times 100 should be exactly 1000) you may
need to do explicid rounding.

REQUIREMENTS
============

* Django (obviously)
* django_deferred_polymorph (may be skipped if you don't use the supplied models)
