# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProfileItem(scrapy.Item):
    # define the fields for your item here like:
    item_name = scrapy.Field()
    _id = scrapy.Field()
    username = scrapy.Field()
    userid = scrapy.Field()
    introduction = scrapy.Field()
    attraction_rate = scrapy.Field()
    height = scrapy.Field()
    weigh = scrapy.Field()
    degree = scrapy.Field()
    blood_type = scrapy.Field()
    nation = scrapy.Field()
    love_state = scrapy.Field()


class RequirementItem(scrapy.Item):
    item_name = scrapy.Field()
    _id = scrapy.Field()
    userid = scrapy.Field()
    age = scrapy.Field()
    height = scrapy.Field()
    nation = scrapy.Field()
    degree = scrapy.Field()
    album = scrapy.Field()
    marriage_state = scrapy.Field()
    live_in = scrapy.Field()
    integrity = scrapy.Field()


class LifeStyleItem(scrapy.Item):
    item_name = scrapy.Field()
    _id = scrapy.Field()
    smoke = scrapy.Field()
    userid = scrapy.Field()
    drink = scrapy.Field()
    exercise_habit = scrapy.Field()
    diet_habit = scrapy.Field()
    shopping = scrapy.Field()
    religious_belief = scrapy.Field()
    schedule = scrapy.Field()
    social_circle = scrapy.Field()
    maximum_consumption = scrapy.Field()


class FinancialSituationItem(scrapy.Item):
    item_name = scrapy.Field()
    _id = scrapy.Field()
    userid = scrapy.Field()
    wage = scrapy.Field()
    house_purchase = scrapy.Field()
    car_purchase = scrapy.Field()
    financial_view = scrapy.Field()
    investment_and_financial_management = scrapy.Field()
    debt_loan = scrapy.Field()


class WorkItem(scrapy.Item):
    item_name = scrapy.Field()
    _id = scrapy.Field()
    userid = scrapy.Field()
    position = scrapy.Field()
    company_category = scrapy.Field()
    company_type = scrapy.Field()
    welfare_treatment = scrapy.Field()
    work_status = scrapy.Field()
    promote_possibility = scrapy.Field()
    work_vs_family = scrapy.Field()
    work_abord_possibility = scrapy.Field()


class EducationItem(scrapy.Item):
    item_name = scrapy.Field()
    _id = scrapy.Field()
    userid = scrapy.Field()
    graduated_from = scrapy.Field()
    major = scrapy.Field()
    language_skill = scrapy.Field()


class MarriageViewItem(scrapy.Item):
    item_name = scrapy.Field()
    _id = scrapy.Field()
    userid = scrapy.Field()
    native_place = scrapy.Field()
    family_location = scrapy.Field()
    nationality = scrapy.Field()
    personality = scrapy.Field()
    sense_of_humor = scrapy.Field()
    temper = scrapy.Field()
    about_child = scrapy.Field()
    about_relationship = scrapy.Field()
    marriage_time = scrapy.Field()
    about_love_in_different_place = scrapy.Field()
    ideal_marriage = scrapy.Field()
    live_with_spouse_family = scrapy.Field()
    kid_situation_in_family = scrapy.Field()
    parents_financial_situation = scrapy.Field()
    sibing_situation = scrapy.Field()
    parents_situation = scrapy.Field()
    parents_work = scrapy.Field()
    health_insurance_about_parents = scrapy.Field()


class ImageItem(scrapy.Item):
    item_name = scrapy.Field()
    userid = scrapy.Field()
    _id = scrapy.Field()
    image_urls = scrapy.Field()
