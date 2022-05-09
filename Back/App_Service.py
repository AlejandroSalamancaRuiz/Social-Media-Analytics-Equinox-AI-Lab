from DataBase import DBConnection
from pymongo import MongoClient
import config

class App_Service():


    def __init__(self):
        self.neo4jDB = DBConnection(config.uri_neo, config.user_neo, config.password_neo)
        self.MongoClient = MongoClient(config.mongo_client)
        self.mongoDB = self.MongoClient.marketingappdb

        self.create_graph()


    def create_graph(self):

        list_followers = list(self.mongoDB.Linkedin_impact.find())

        list_posts = list(self.mongoDB.Linkedin.find())

        dict_followers = list_followers[0]

        list_followers = dict_followers['seguidores']


        with self.neo4jDB.driver.session() as session:

            for follower in list_followers:

                name = follower[0]
                num_followers = follower[1]
                description = follower[2]
                date = follower[3]

                session.write_transaction(self.neo4jDB.create_node_person, name, num_followers, description, date)


            for dict_post in list_posts:

                post = dict_post['publicacion']
                date = dict_post['fecha']
                repost = dict_post['repost']
                clicks = ((dict_post['clicks'])[-1:])[0][0]

                session.write_transaction(self.neo4jDB.create_node_post, post, date, repost, clicks)

                for reaction in dict_post['reacciones']:

                    name = reaction[0]
                    date_reaction = reaction[1]

                    session.write_transaction(self.neo4jDB.create_edge_reaction, name, post, date_reaction)



    def recommend_post_to_user(self, user, num_posts):

        recommended_posts = {}
        recommended_posts['posts'] = []


        with self.neo4jDB.driver.session() as session:

            list_posts = session.write_transaction(self.neo4jDB.recomend_post, user)

        if list_posts is None:
            recommended_posts['posts'].append('No followers with that name')

        else:

            for i in range(num_posts):
                recommended_posts['posts'].append(list_posts[i][0])

        return recommended_posts


    def people_interested_in_topic(self, topic, num_people):

        people = {}
        people['name'] = []
        people['reactions to related posts'] = []
        people['followers'] = []

        with self.neo4jDB.driver.session() as session:

            list_people = session.write_transaction(self.neo4jDB.people_interested_in_topic, topic)

        if list_people:

            for i in range(num_people):
                people['name'].append(list_people[i][0])
                people['reactions to related posts'].append(list_people[i][1])
                people['followers'].append(list_people[i][2])

        else:

            people['name'].append('No match for topic')
            people['reactions to related posts'].append(' ')
            people['followers'].append(' ')


        return people


    def find_interests(self, profile, num_posts):

        posts = {}
        posts['post'] = []

        with self.neo4jDB.driver.session() as session:

            list_posts = session.write_transaction(self.neo4jDB.find_interests, profile)

        if list_posts:

            for i in range(num_posts):

                posts['post'].append(list_posts[i][1])


        else:

            posts['post'].append('No match')

        return posts


    def num_followers(self, profile):

        followers = {}
        followers['num'] = []

        with self.neo4jDB.driver.session() as session:

            num_followers = session.write_transaction(self.neo4jDB.num_followers, profile)

        if num_followers:

            followers['num'] = num_followers

        else:

            followers['num'] = ['No followers with that description']

        return followers


    def followers_reach(self, profile):

        followers = {}
        followers['reach'] = []

        with self.neo4jDB.driver.session() as session:

            reach = session.write_transaction(self.neo4jDB.followers_reach, profile)

        if reach:

            followers['reach'] = reach

        else:

            followers['reach'] = ['No followers with that description']

        return followers


    def influential_taste(self, num_posts):

        posts = {}
        posts['post'] = []

        with self.neo4jDB.driver.session() as session:

            list_posts = session.write_transaction(self.neo4jDB.influential_taste)

        if posts:

            for i in range(num_posts):

                posts['post'].append(list_posts[i][1])


        return posts







