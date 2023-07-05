from sqlalchemy.orm import relationship

from datetime import datetime
from distutils.sysconfig import get_makefile_filename
from sqlalchemy import (
    Column, BigInteger,
    String, Integer,
    DateTime, Text, ForeignKey
    )

from tgbot.db.base import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    username = Column(String(50))
    first_name = Column(String(50))


class School(Base):
    __tablename__ = "school"

    id = Column(Integer, primary_key=True)
    nomi = Column(String(150))
    malumot = Column(Text)
    rahbariyat = Column(Text)
    yonalish = Column(Text)
    qabul = Column(String(150))
    savollar = Column(Text)
    boglanish = Column(Text)


class College(Base):
    __tablename__ = "college"

    id = Column(Integer, primary_key=True)
    nomi = Column(String(150))
    malumot = Column(Text)
    rahbariyat = Column(Text)
    yonalish = Column(Text)
    qabul = Column(String(150))
    savollar = Column(Text)
    boglanish = Column(Text)


class Texnikum(Base):
    __tablename__ = "texnikum"

    id = Column(Integer, primary_key=True)
    nomi = Column(String(150))
    malumot = Column(Text)
    rahbariyat = Column(Text)
    yonalish = Column(Text)
    qabul = Column(String(150))
    savollar = Column(Text)
    boglanish = Column(Text)


class Lyceum(Base):
    __tablename__ = "lyceum"

    id = Column(Integer, primary_key=True)
    nomi = Column(String(150))
    malumot = Column(Text)
    rahbariyat = Column(Text)
    yonalish = Column(Text)
    qabul = Column(String(150))
    savollar = Column(Text)
    boglanish = Column(Text)


class CorrupsionIssue(Base):
    __tablename__ = "corrupsionissue"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    username = Column(String(150))
    name = Column(String(150))
    contact = Column(String(150))
    issue = Column(Text)