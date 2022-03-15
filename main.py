from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import datetime


url = 'https://www.hltv.org/matches?predefinedFilter=top_tier'
url_results = 'https://www.hltv.org/results'


def get_pars_page(url):
    ua = UserAgent()
    headers = {
        'User-Agent':ua.random,
        'content-type': 'text/html;charset=utf-8'
    }
    page = requests.get(url, headers=headers)
    return BeautifulSoup(page.text, 'html.parser')
    

def upcoming_game():
    upcoming_game = []
    for item in get_pars_page(url).find_all('div', class_='upcomingMatch'):
        try:
            date_game = [i['data-unix'] for i in item.find_all('div', {'class':'matchTime'})][0]
            team_1, team_2 = (i.text for i in item.find_all('div', class_='matchTeamName text-ellipsis'))
            event_name = item.find('div', class_='matchEventName gtSmartphone-only').text
            upcoming_game.append(
                {'date_game': datetime.datetime.fromtimestamp(int(date_game) // 1000),
                'team_1': team_1,
                'team_2': team_2,
                'event_name': event_name,
                }
            )
        except ValueError:
            continue
    return upcoming_game


def live_game():
    live_game = []
    for item in get_pars_page(url).find_all('div', class_='liveMatch-container'):
        team_1, team_2 = (i.text for i in item.find_all('div', class_='matchTeamName text-ellipsis'))
        event_name = item.find('div', class_='matchEventName gtSmartphone-only').text
        live_game.append(
                {'team_1': team_1,
                'team_2': team_2,
                'event_name': event_name,
                }
            )
    return live_game
    

def results_game():
    results = []
    for item in get_pars_page(url_results).find_all('div', class_='result-con')[0:8]:
        team_won = item.find('div', class_='team team-won').text
        team_loser = [i for i in item.find_all('div', class_='team') if i.text != team_won][0].text
        score_won = item.find('span', class_='score-won').text
        score_loser = item.find('span', class_='score-lost').text
        event_name = item.find('span', class_='event-name').text
        results.append(
            {'team_won': team_won,
            'team_loser': team_loser,
            'score_won': score_won,
            'score_loser': score_loser,  
            'event_name': event_name, 
            }
        )
    return results


def main():
    upcoming_game()
    live_game()
    results_game()
    
    
if __name__ == '__main__':
    main()
    

