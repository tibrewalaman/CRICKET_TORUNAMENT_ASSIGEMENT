import random
import os
class Player:
    def __init__(self, name, bowling, batting, fielding, running, experience):
        """
        Represents a player in a cricket team.
        Initialize a Player object with the provided attributes.
        
        """
        self.name = name
        self.bowling = bowling
        self.batting = batting
        self.fielding = fielding
        self.running = running
        self.experience = experience

class Team:

    def __init__(self, name, players):
        """
        Initialize a Team object with the provided attributes.
        
        """
        self.name = name
        self.players = players
        self.captain = None
        self.batting_order = players.copy()
        self.bowlers = []

    def select_captain(self, captain):
        """
        Select the captain for the team.
        
        """
        self.captain = captain

    def sending_next_player(self):
        """
        Send the next player from the batting order.
        
        """
        if len(self.batting_order)>0:
            return self.batting_order.pop(0)
        return None 
    
    def choose_bowler(self):
        """
        Choose a bowler randomly from the team's bowlers.
        
        """
        return random.choice(self.bowlers)
    

class Field:
    def __init__(self, size, fan_ratio, pitch_conditions, home_advantage):
        """
        Initialize a Field object with the provided attributes.
        
        """
        self.size = size
        self.fan_ratio = fan_ratio
        self.pitch_conditions = pitch_conditions
        self.home_advantage = home_advantage


class Umpire:
    def __init__(self, field):
        """
        Initialize an Umpire object with the provided attributes.
        
        """
        self.field = field
        self.scores = 0
        self.wickets = 0
        self.overs = 0

    def update_score(self, runs):
        """
        Update the score based on the runs scored.
        
        """
        self.scores += runs

    def update_wickets(self):
        """
        Update the wickets count.
        
        """
        self.wickets += 1

    def update_overs(self):
        """
        Update the overs count.
        
        """
        self.overs += 1

    def predict_outcome(self, batsman, bowler):
        """
        Predict the outcome of a ball based on batsman and bowler stats.
    
        """
        batting_prob = batsman.batting * self.field.pitch_conditions * random.random()
        bowling_prob = bowler.bowling * self.field.pitch_conditions * random.random()
        if batting_prob > bowling_prob:
            return "OUT"
        return "NOT OUT"

class Commentator:
    def __init__(self, umpire):
        """
        Initialize a Commentator object with the provided attributes.
        
        """
        self.umpire = umpire

    def describe_ball(self, batsman, bowler):
        """
        Generate a description of the ball played by the batsman.

        """
        outcome = self.umpire.predict_outcome(batsman, bowler)
        print("Outcome: ", outcome)
        if outcome == "OUT":
            description = f"{batsman.name} is OUT!"
        else:
            description = f"{batsman.name} plays the shot."

        return description

    def describe_game(self, captain1, captain2, country1, country2, over):
        """
        Provide a description of the cricket match.
        
        """
        print("\n--------- Game Information ---------\n")
        print(f"{country1} Vs {country2}")
        print(f"Captain 1 : {captain1}, Captain 2 : {captain2}")
        print(f"Over : {over}")
        print("\n---------------------------------------------\n")

    def describe_start(self, team):
        """
        Provide a description of the start of an innings.
        
        """
        print("\n------------- GAME STARTED ------------------\n")
        print(f"Team {team} playing: ")
    
    def describe_end(self):
        """
        Provide a description of the end of an innings.
        
        """
        print(f"\n\nFinal Run: {self.umpire.scores} Wicket: {self.umpire.wickets} Overs: {self.umpire.overs}")
        print("\n---------------------------------------------\n")

    
    def current_info(self, ball_count):
        """
        Provide the current match information.
        
        """
        print(f"Balls: {ball_count} Over: {self.umpire.overs} Run: {self.umpire.scores}  Wicket: {self.umpire.wickets}")

    def describe_final_result(self, name, scores):
        """
        Provide a description of the final result of the match.
        
        """
        print("--------------- Winner -----------------------")
        print(f"TEAM : {name} WON BY SCORE: {scores}")
        print("\n---------------------------------------------\n")

class Match:
    def __init__(self, team1, team2, field, total_overs):
        """
        Represents a cricket match between two teams.
        
        """
        self.team1 = team1
        self.team2 = team2
        self.field = field
        self.umpire = Umpire(field)
        self.commentator = Commentator(self.umpire)
        self.total_overs = total_overs

    def start_match(self):
        """
        Starts the cricket match.
        
        """
        self.team1.select_captain(random.choice(self.team1.players))
        self.team2.select_captain(random.choice(self.team2.players))
        self.team1.batting_order = self.team1.players.copy()
        self.team2.batting_order = self.team2.players.copy()
        self.team1.bowlers = self.team1.players.copy()
        self.team2.bowlers = self.team2.players.copy()

        self.commentator.describe_game(self.team1.captain.name, self.team2.captain.name, self.team1.name, self.team2.name, over=self.total_overs)

        # Team 1 playing    
        self.commentator.describe_start(self.team1.name)
        self.play_innings(self.team1, self.team2)
        self.commentator.describe_end()
        lastScores = self.commentator.umpire.scores


        # Team 2 playing    
        self.commentator.umpire.scores = 0
        self.commentator.umpire.wickets = 0
        self.commentator.umpire.overs = 0
        self.commentator.describe_start(self.team2.name)
        self.play_innings(self.team2, self.team1)
        self.commentator.describe_end()
        newScores = self.commentator.umpire.scores

        # Final outcome
        if lastScores > newScores:
            self.commentator.describe_final_result(total_team_list[z].name, lastScores)
            return total_team_list[z]
        else:
            self.commentator.describe_final_result(total_team_list[z+1].name, newScores)
            return total_team_list[z+1]


    def play_innings(self, batting_team, bowling_team):
        """
        Simulates the innings of a team.
        
        """
        ball_count = 1
        over = 0
        bowler = bowling_team.choose_bowler() 
        batsman = batting_team.sending_next_player()
        
        while over < self.total_overs:
            print("\n")
            self.commentator.current_info(ball_count)
            ball_description = self.commentator.describe_ball(batsman, bowler)
            
            print(ball_description)
            if ball_description.endswith("OUT!"):
                batsman = batting_team.sending_next_player()
                if batsman is None:
                    break
                self.umpire.update_wickets()
                print(f"Wickets: {self.umpire.wickets} , Overs: {self.umpire.overs}")
                print(f"New player {batsman.name} is playing...")
            else:
                runs = random.randint(0, 6)
                self.umpire.update_score(runs)

            if ball_count > 5:
                over += 1
                print(f"Over {over} Starting...")
                self.umpire.update_overs()
                bowler = bowling_team.choose_bowler()
                ball_count = 0

            self.commentator.current_info(ball_count)
            ball_count += 1



            
            
#Loading  files for names for teams and players
file=open("name.txt","r")
name_list=str(file.readlines()).split("\\n")
file2=open("teams.txt","r")
team_list=str(file2.readlines()).split("\\n")


#Adding overs and players in the game
player_list=[]
number_of_teams=13
total_overs=21


#Taking input for number of teams and overs
while number_of_teams>12 or number_of_teams<2 or total_overs<2 or total_overs>20:
    number_of_teams=int(input("ENTER NUMBER OF TEAMS(DO NOT ENTER MORE THE 12 ) :   "))
    print("---------------------------\n\n")
    total_overs =int(input("ENTER THE NUMBER OF OVERS(BETWEEN 2 TO 20) :   "))
    if number_of_teams>12 and number_of_teams<2:
        print("Please enter number between 2 to 12")
        print("---------------------------\n\n")
    if total_overs<2 and total_overs>20:
        print("please enter the over between 2 and 20")
        print("---------------------------\n\n")
        

# Creating  players for  the game
for  j in range(number_of_teams):
    player_in_team = []
    for i in range(10):
        random_name=random.choice(name_list)
        player_in_team.append(Player(random_name, round(random.random(),1), round(random.random(),1),round(random.random(),1), round(random.random(),1), round(random.random(),1)))
        name_list.remove(random_name)
    player_list.append(player_in_team)
file.close()

# Adding players to team
total_team_list=[]
for k in player_list:
    random_team_name=random.choice(team_list)
    total_team_list.append(Team(random_team_name, k))
    team_list.remove(random_team_name)
file2.close()


#Starting the Tournament
while len(total_team_list) >1:
    next_round_list=[]
    number_of_iteration=len(total_team_list)
    
    # starting match simulation
    for z in range(0,number_of_iteration-1,2):
        
        # Making a random  field
        field_size=["Large","Small","Medium"]
        field_stats=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
        field = Field(random.choice(field_size),random.choice(field_stats),random.choice(field_stats),random.choice(field_stats))
        
        
        if number_of_iteration%2 == 1:
            next_round_list.append(total_team_list[len(total_team_list)-1])
            number_of_iteration=number_of_iteration-1
        match = Match(total_team_list[z], total_team_list[z+1], field, total_overs)
        
        #Creating a list of Winner of the first round
        next_round_list.append(match.start_match())
        
    #Updating the Total number teams in the tournament
    total_team_list=next_round_list
    
#Announcing the winner of the tournament
print("-------------Tournament Winner-------------\n\n")
print("TEAM : ",total_team_list[0].name)