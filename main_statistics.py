
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from DataFunctions import select_datadetail
from Globals import *
import math


def generate_graphs_1(vyear,vteam):
  
    year = vyear
    iduser = getIDUser()
    team = vteam
    result, data = select_datadetail(year, iduser)
    
    if result == True:
            plt.rcParams['figure.dpi'] = 96
            plt.rcParams['savefig.dpi'] = 96 
    
            plt.close()  
            teams = list(set(data['Home Team']).union(set(data['Away Team'])))
          
            home_goals = data.groupby('Home Team')['Score'].apply(lambda x: sum([int(s.split('-')[0]) for s in x])).to_dict()
            away_goals = data.groupby('Away Team')['Score'].apply(lambda x: sum([int(s.split('-')[1]) for s in x])).to_dict()
            
            home_fouls = data.groupby('Home Team')['Match Excitement'].apply(lambda x: x.count()).to_dict()
            away_fouls = data.groupby('Away Team')['Match Excitement'].apply(lambda x: x.count()).to_dict()

            
            width_in_inches = 1250 / 96  
            height_in_inches = 600 / 96  
            
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(width_in_inches, height_in_inches), dpi=96)  

            x = range(len(teams))

            ax1.bar(x, [home_goals.get(e, 0) for e in teams], width=0.3, label='Goals scored (Home)', align='center')

            ax1.bar(x, [away_goals.get(e, 0) for e in teams], width=0.3, label='Goals scored (Away)', 
                    bottom=[home_goals.get(e, 0) for e in teams], align='center')

            ax1.bar(x, [home_fouls.get(e, 0) + away_fouls.get(e, 0) for e in teams], width=0.3, label='Fouls committed', alpha=0.5, align='center')

            ax1.set_xticks(x)
            ax1.set_xticklabels(teams, rotation=90, fontsize=8)  

            ax1.set_xlim(-0.5, len(teams) - 0.5)

            ax1.set_title("Goals and Fouls per Team" +" year: " + str(year))
           
            ax1.legend()

            metrics = ['Home Team Possession %', 'Home Team Off Target Shots', 'Home Team On Target', 
                    'Away Team Possession %', 'Away Team Off Target Shots']

            values = [
                data[data['Home Team'] == team][metric].mean() if metric in data.columns else 0 for metric in metrics
            ]
            
            values.append(values[0])

            categories = metrics + [metrics[0]]

            angles = [i / float(len(categories)) * 2 * math.pi for i in range(len(categories))]

            ax2 = fig.add_subplot(122, polar=True)
            ax2.fill(angles, values, alpha=0.25)
            ax2.plot(angles, values, label=team)
            ax2.set_title(f"Performance of Team: {team}")
            ax2.set_xticks(angles[:-1])  
            ax2.set_xticklabels(categories[:-1], rotation=45)

            filename="graph_2.png"
            plt.savefig(filename,dpi=96) 
            displayer(filename)


def generate_graphs_2(vyear,vteam):
  
    year = vyear
    iduser = getIDUser()   
    result, data = select_datadetail(year, iduser)
    
    if result == True:
        plt.rcParams['figure.dpi'] = 96
        plt.rcParams['savefig.dpi'] = 96      
        plt.close()  
        home_data = data[data['Home Team'] == vteam]
        away_data = data[data['Away Team'] == vteam]
        
        if home_data.empty and away_data.empty:            
            return

        home_goals = home_data['Home Team Goals Scored']
        away_goals = away_data['Away Team Goals Scored']
        home_possession = home_data['Home Team Possession %']
        away_possession = away_data['Away Team Possession %']
        home_shots_on_target = home_data['Home Team On Target Shots']
        away_shots_on_target = away_data['Away Team On Target Shots']
        
        width_in_inches = 1250 / 96 
        height_in_inches = 600/ 96  
      
        fig, ax = plt.subplots(figsize=(width_in_inches, height_in_inches), dpi=96)  
       
        if not home_data.empty:
            ax.scatter(home_possession, home_goals, s=home_shots_on_target * 10, alpha=0.5, label=f'{vteam} (Home)', c='blue')        
        if not away_data.empty:
            ax.scatter(away_possession, away_goals, s=away_shots_on_target * 10, alpha=0.5, label=f'{vteam} (Away)', c='red')
        ax.set_xlabel('Possession (%)')
        ax.set_ylabel('Goals Scored')
        ax.set_title(f'Comparison of Goals Scored vs Possession and Shots on Target for {vteam} year: {year}')
        ax.legend()        
        filename="graph_2.png"
        plt.savefig(filename,dpi=96) 
        displayer(filename)


def plot_shots(vyear):
    year = vyear
    iduser = getIDUser()
    result, data = select_datadetail(year, iduser)
    
    if result == True:
        home_on_target = data.groupby('Home Team')['Home Team On Target Shots'].sum()
        away_on_target = data.groupby('Away Team')['Away Team On Target Shots'].sum()
        home_off_target = data.groupby('Home Team')['Home Team Off Target Shots'].sum()
        away_off_target = data.groupby('Away Team')['Away Team Off Target Shots'].sum()
        home_blocked_shots = data.groupby('Home Team')['Home Team Blocked Shots'].sum()
        away_blocked_shots = data.groupby('Away Team')['Away Team Blocked Shots'].sum()
        home_total_shots = data.groupby('Home Team')['Home Team Total Shots'].sum()
        away_total_shots = data.groupby('Away Team')['Away Team Total Shots'].sum()
        
        home_shots = [home_on_target, home_blocked_shots, home_off_target]
        away_shots = [away_on_target, away_blocked_shots, away_off_target]
        
        teams = sorted(set(data['Home Team']).union(set(data['Away Team'])))
        index = range(len(teams))
        
        width_in_inches = 1250 / 96  
        height_in_inches = 600/ 96  
        fig =plt.figure(figsize=(width_in_inches, height_in_inches), dpi=96)
            
        ax3 = fig.add_subplot(111)  
        
        ax3.bar(index, home_shots[0], label='Home Team On Target', color='green')
        ax3.bar(index, home_shots[1], bottom=home_shots[0], label='Home Team Blocked', color='purple')
        ax3.bar(index, home_shots[2], bottom=[i + j for i, j in zip(home_shots[0], home_shots[1])], label='Home Team Off Target', color='blue')
        ax3.bar([i + 0.4 for i in index], away_shots[0], label='Away Team On Target', color='orange')
        ax3.bar([i + 0.4 for i in index], away_shots[1], bottom=away_shots[0], label='Away Team Blocked', color='yellow')
        ax3.bar([i + 0.4 for i in index], away_shots[2], bottom=[i + j for i, j in zip(away_shots[0], away_shots[1])], label='Away Team Off Target', color='red')
        
        ax3.set_xlabel('Teams')
        ax3.set_ylabel('Shots')
        ax3.set_title(f'Stacked Bar Chart of Shots (Home vs Away) year: {year}')
        ax3.set_xticks([i + 0.2 for i in index])  
        ax3.set_xticklabels(teams, rotation=45)
        ax3.legend()
        filename="graph_2.png"
        plt.savefig(filename,dpi=96) 
        displayer(filename)

    else:
        print("Failed to fetch data!")
        
        
        
        
def displayer(filename):
    from Dashboard import statistics
    win = GraphWin("Show",1200, 600)
    win.setBackground('dark green')
    bg_image = Image(Point(600, 300), filename)       
    
    bg_image.draw(win)
    done, done_writting  = create_button(win, Point(1080, 10), Point(1180, 50), "Done", "green", "white",size=10)    
    
    while True:
        click = win.getMouse()
        if is_click_in_rectangle(click,done):
            win.close()
            statistics(getIDUser())
           
