from neo4j import GraphDatabase

class DBConnection:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node_person(self, tx, name, num_followers, description, date):
        tx.run("CREATE (p:Person {name: $name, num_followers: $num_followers, \
                description: $description, date: $date})",name=name, num_followers=num_followers,
               description=description, date=date)

    def create_node_post(self, tx, post, date, repost, clicks):
        tx.run("CREATE (p:Post {post: $post, date: $date, \
                repost: $repost, clicks: $clicks})",post=post, date=date,
               repost=repost, clicks=clicks)

    def find_node(self, tx, name):
        ans = tx.run("MATCH (a:Person) WHERE a.name = $name RETURN NOT EXISTS(a.name)", name=name)

        if str(type(ans.single())) == "<class 'NoneType'>":
            return False

        else:

            return True


    def create_edge_reaction(self, tx, node_person, node_post, date):

        exists = self.find_node(tx, node_person)

        if not exists:
            self.create_node_person(tx, node_person, None, None, None)

        tx.run("MATCH (a:Person), (b:Post) WHERE a.name = $nameA AND b.post = $nameB \
                CREATE (a)-[r:Reaction {date: $date}]->(b)", nameA = node_person, nameB = node_post, date = date)



    def recomend_post(self, tx, node_person):

        exists = self.find_node(tx, node_person)

        if not exists:
            return None

        else:

            ans = tx.run("MATCH (p:Person {name: $name_user})-[:Reaction]->(post0: Post)<-[:Reaction]-(p2:Person) -[:Reaction]->(post1:Post) \
                        WHERE p <> p2 \
                        AND NOT (p)-[:Reaction]->(post1)<-[:Reaction]-(p2) \
                        RETURN post1.post, count(post1) as count \
                        ORDER BY count DESC", name_user=node_person)

            list_ans = []

            for row in ans:
                list_ans.append([row[0], row[1]])

            return list_ans


    def people_interested_in_topic(self, tx, topic):

        ans = tx.run("match (post:Post)<-[:Reaction]-(p1:Person) \
                    where toLower(post.post) contains $topic \
                    return p1.name, count(p1) as count, p1.num_followers \
                    order by count desc", topic=topic)

        list_ans = []

        for row in ans:
            list_ans.append([row[0], row[1], row[2]])

        return list_ans


    def find_interests(self, tx, profile):

        ans = tx.run("match (post:Post)<-[:Reaction]-(p1:Person) \
                    where toLower(p1.description) contains $profile \
                    return count(post) as count, post.post \
                    order by count desc;", profile=profile)

        list_ans = []

        for row in ans:
            list_ans.append([row[0], row[1]])

        return list_ans


    def num_followers(self,tx, profile):

        ans = tx.run("match (p:Person) \
                    where toLower(p.description) contains $profile \
                    return count(p)", profile=profile )

        list_ans = []

        for row in ans:
            list_ans.append([row[0]])

        return list_ans

    def followers_reach(self,tx, profile):

        ans = tx.run("match (p:Person) \
                    where toLower(p.description) contains $profile \
                    return sum(toInteger(p.num_followers))", profile=profile )

        list_ans = []

        for row in ans:
            list_ans.append([row[0]])

        return list_ans

    def influential_taste(self,tx):

        ans = tx.run("match (post:Post)<-[:Reaction]-(p1:Person) \
                    where p1.num_followers = '500' \
                    return count(post), post.post")

        list_ans = []

        for row in ans:
            list_ans.append([row[0], row[1]])

        return list_ans

