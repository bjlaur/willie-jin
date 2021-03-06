# coding=utf8
"""
"""
from __future__ import unicode_literals

import re
from willie.tools import Identifier, WillieMemory
from willie.module import rule, priority, commands
from willie.formatting import bold



def setup(bot):
    bot.memory['jin_memory'] = WillieMemory()


@rule('.*')
@priority('low')
def collectlines(bot, trigger):
    """Create a temporary log of what people say"""

    if trigger.is_privmsg:
        return

    numlines = 75 #TODO: Config
    owner = 'Byan' #TODO: We shouldn't need to hardcode this
    quiet = ('QUIET',)
    people = ['jin', 'common', 'tm512'] + [owner] + [quiet]
    threshold = .28
    
    if 'lines' not in bot.memory['jin_memory']:
        bot.memory['jin_memory']['lines'] = list()

    tmplines = bot.memory['jin_memory']['lines']
    tmplines.append(str(trigger.nick))

    if len(tmplines) > numlines:
        tmplines.pop(0)

    bot.memory['jin_memory']['lines'] = tmplines #TODO: We shouldn't need to save twice, but I want to use returns and python don't have GOTOs

    #TODO: We should be able to cache this and not reierate over the list every time.
    count = dict()

    for x in tmplines:
#if x in people:
        if True:
            if x not in count.keys():
                count[x] = 1
            else:
                count[x] = count[x] + 1
    
    bot.memory['jin_memory']['count'] = count
    print(count)

    if quiet in count:
        return

    if len(tmplines) < numlines:
        return

    if owner not in count.keys() or count[owner]/numlines <= threshold:
        return

    del count[owner]

    for dick in count.keys():
        if dick not in people:
            continue
        if count[dick]/numlines > threshold:
            bot.notice("You might be talking to %s too much" % dick, owner)
            tmplines.append(quiet)
            
    
    bot.memory['jin_memory']['lines'] = tmplines



@commands('metrics', 'm')
def metrics(bot, trigger):
    bot.reply(bot.memory['jin_memory']['count'])
