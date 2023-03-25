# Author: Afnan

from sqlalchemy import Table, Column, Integer, ForeignKey

tickets_tags = Table("tickets_tags",
                       Column('ticket_id', Integer, ForeignKey('ticket.id')),
                       Column('tag_id', Integer, ForeignKey('tag.id'))
                       )