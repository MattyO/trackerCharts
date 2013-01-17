#from splinter import Browser
from zope.testbrowser.browser import Browser
from lettuce import *
from pyquery import PyQuery as py

@step('Given Im on the index page')
def on_index_page(step):
	world.browser = Browser()
	world.browser.open("http://localhost:4567")

@step(u'And there are some users')
def and_there_are_some_users(step):
	world.number_of_users = 1

@step(u'Then there should be the same number of bars')
def then_there_should_be_the_same_number_of_bars(step):
		jq = py(world.browser.contents)
		assert len(jq("h1")) == 2
		
		#assert world.number_of_users == len(jq("#wip.chart").find("rect"))
