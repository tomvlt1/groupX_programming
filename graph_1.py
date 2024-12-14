
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from DataFunctions import select_datadetail
from Globals import *
import math

def generate_graphs_1(vyear,vteam):
  
    year = vyear
    iduser = getIDUser()
    team = vteam
    result, data = select_datadetail(year, iduser)
    
    if result == True:
            # Calculate goals and fouls per team by selecting the list of teams that are both home and away teams.            
            teams = list(set(data['Home Team']).union(set(data['Away Team'])))
          
            # Calculate goals scored
            home_goals = data.groupby('Home Team')['Score'].apply(lambda x: sum([int(s.split('-')[0]) for s in x])).to_dict()
            away_goals = data.groupby('Away Team')['Score'].apply(lambda x: sum([int(s.split('-')[1]) for s in x])).to_dict()
            
            # Calculate fouls (assumed as match excitement for simplicity)
            home_fouls = data.groupby('Home Team')['Match Excitement'].apply(lambda x: x.count()).to_dict()
            away_fouls = data.groupby('Away Team')['Match Excitement'].apply(lambda x: x.count()).to_dict()

            # Create subplots: 1 row, 2 columns
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10))  # Increased width to accommodate all teams

            # Bar chart on the first axis (ax1)
            x = range(len(teams))

            # Home team goals
            ax1.bar(x, [home_goals.get(e, 0) for e in teams], width=0.3, label='Goals scored (Home)', align='center')

            # Away team goals
            ax1.bar(x, [away_goals.get(e, 0) for e in teams], width=0.3, label='Goals scored (Away)', 
                    bottom=[home_goals.get(e, 0) for e in teams], align='center')

            # Fouls committed
            ax1.bar(x, [home_fouls.get(e, 0) + away_fouls.get(e, 0) for e in teams], width=0.3, label='Fouls committed', alpha=0.5, align='center')

            # Rotate x-tick labels for better readability
            ax1.set_xticks(x)
            ax1.set_xticklabels(teams, rotation=90, fontsize=8)  # Smaller font size

            # Set the x-axis limits to ensure all labels fit
            ax1.set_xlim(-0.5, len(teams) - 0.5)

            ax1.set_title("Goals and Fouls per Team" +" year: " + str(year))
           
            ax1.legend()

            # Radar chart on the second axis (ax2)
            metrics = ['Home Team Possession %', 'Home Team Off Target Shots', 'Home Team On Target', 
                    'Away Team Possession %', 'Away Team Off Target Shots']

            # Get average values for radar chart
            values = [
                data[data['Home Team'] == team][metric].mean() if metric in data.columns else 0 for metric in metrics
            ]
            
            # Append first value to close the circle
            values.append(values[0])

            # Categories include first metric again to close the circle
            categories = metrics + [metrics[0]]

            # Calculate angles for each category
            angles = [i / float(len(categories)) * 2 * math.pi for i in range(len(categories))]

            # Create radar chart on ax2
            ax2 = fig.add_subplot(122, polar=True)
            ax2.fill(angles, values, alpha=0.25)
            ax2.plot(angles, values, label=team)
            ax2.set_title(f"Performance of Team: {team}")
            ax2.set_xticks(angles[:-1])  # Exclude the last label as it is the same as the first
            ax2.set_xticklabels(categories[:-1], rotation=45)

            # Show both charts at once
            plt.tight_layout()  # Adjust layout to avoid overlap
            plt.show()


def generate_graphs_2(vyear,vteam):
  
    year = vyear
    iduser = getIDUser()   
    result, data = select_datadetail(year, iduser)
    
    if result == True:
        # Filter
        home_data = data[data['Home Team'] == vteam]
        away_data = data[data['Away Team'] == vteam]
        
        # Check
        if home_data.empty and away_data.empty:            
            return

        # Extract data
        home_goals = home_data['Home Team Goals Scored']
        away_goals = away_data['Away Team Goals Scored']
        home_possession = home_data['Home Team Possession %']
        away_possession = away_data['Away Team Possession %']
        home_shots_on_target = home_data['Home Team On Target Shots']
        away_shots_on_target = away_data['Away Team On Target Shots']
        
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 6))        
        
        if not home_data.empty:
            ax.scatter(home_possession, home_goals, s=home_shots_on_target * 10, alpha=0.5, label=f'{vteam} (Home)', c='blue')        
        if not away_data.empty:
            ax.scatter(away_possession, away_goals, s=away_shots_on_target * 10, alpha=0.5, label=f'{vteam} (Away)', c='red')
        # label and title
        ax.set_xlabel('Possession (%)')
        ax.set_ylabel('Goals Scored')
        ax.set_title(f'Comparison of Goals Scored vs Possession and Shots on Target for {vteam} year: {year}')
        ax.legend()        
        plt.show()


def plot_shots(vyear):
    year = vyear
    iduser = getIDUser()
    result, data = select_datadetail(year, iduser)
    
    if result == True:
        # Group by Home Team and Away Team for shots statistics
        home_on_target = data.groupby('Home Team')['Home Team On Target Shots'].sum()
        away_on_target = data.groupby('Away Team')['Away Team On Target Shots'].sum()
        home_off_target = data.groupby('Home Team')['Home Team Off Target Shots'].sum()
        away_off_target = data.groupby('Away Team')['Away Team Off Target Shots'].sum()
        home_blocked_shots = data.groupby('Home Team')['Home Team Blocked Shots'].sum()
        away_blocked_shots = data.groupby('Away Team')['Away Team Blocked Shots'].sum()
        home_total_shots = data.groupby('Home Team')['Home Team Total Shots'].sum()
        away_total_shots = data.groupby('Away Team')['Away Team Total Shots'].sum()
        
        # Create the data for the stacked bar chart
        home_shots = [home_on_target, home_blocked_shots, home_off_target]
        away_shots = [away_on_target, away_blocked_shots, away_off_target]
        
        teams = sorted(set(data['Home Team']).union(set(data['Away Team'])))
        index = range(len(teams))
        
        # Create a figure with only the stacked bar chart
        fig = plt.figure(figsize=(18, 6))  # Adjusted to make it wide
        ax3 = fig.add_subplot(111)  # Only one axis for the stacked bar chart
        
        # Stacked Bar Chart (Home vs Away Shots)
        ax3.bar(index, home_shots[0], label='Home Team On Target', color='green')
        ax3.bar(index, home_shots[1], bottom=home_shots[0], label='Home Team Blocked', color='purple')
        ax3.bar(index, home_shots[2], bottom=[i + j for i, j in zip(home_shots[0], home_shots[1])], label='Home Team Off Target', color='blue')
        ax3.bar([i + 0.4 for i in index], away_shots[0], label='Away Team On Target', color='orange')
        ax3.bar([i + 0.4 for i in index], away_shots[1], bottom=away_shots[0], label='Away Team Blocked', color='yellow')
        ax3.bar([i + 0.4 for i in index], away_shots[2], bottom=[i + j for i, j in zip(away_shots[0], away_shots[1])], label='Away Team Off Target', color='red')
        
        ax3.set_xlabel('Teams')
        ax3.set_ylabel('Shots')
        ax3.set_title(f'Stacked Bar Chart of Shots (Home vs Away) year: {year}')
        ax3.set_xticks([i + 0.2 for i in index])  # Position the team names correctly
        ax3.set_xticklabels(teams, rotation=45)
        ax3.legend()

        # Show the plot
        plt.tight_layout()
        plt.show()

    else:
        print("Failed to fetch data!")